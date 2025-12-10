import sys

from autospec.decomposition import ExtendedCallGraphBuilder


if __name__ == "__main__":
    c_code = """
    #include <stdio.h>

    void leaf_function() {
        printf("I am a leaf\\n");
    }

    void helper() {
        leaf_function();
    }

    void process_data() {
        for (int i = 0; i < 5; i++) {
            helper();
        }
    }

    int main() {
        int x = 0;
        while (x < 3) {
            process_data();
            x++;
        }
        return 0;
    }
    """

    print("--- Initializing Builder starting at 'main' (Line 18) ---")

    try:
        builder = ExtendedCallGraphBuilder(c_code, start_line=18)

        step_count = 1
        print("--- Traversing Bottom-Up ---")
        while True:
            node = builder.next()
            if node is None:
                break

            print(f"\n[Step {step_count}] Visiting: {node}")

            annotated = builder.annotate_node(node)
            print(annotated)  # Uncomment to see full source

            step_count += 1

        print("\n--- Final Edges ---")
        for src, dst in builder.graph_edges:
            print(f"{src.name} -> {dst.name}")

    except Exception as e:
        print(f"Error: {e}")
import sys

from autospec.decomposition import ExtendedCallGraphBuilder


if __name__ == "__main__":
    c_code = """
    #include <stdio.h>

    void leaf_function() {
        printf("I am a leaf\\n");
    }

    void helper() {
        leaf_function();
    }

    void process_data() {
        for (int i = 0; i < 5; i++) {
            helper();
        }
    }

    int main() {
        int x = 0;
        while (x < 3) {
            process_data();
            x++;
        }
        return 0;
    }
    """

    print("--- Initializing Builder starting at 'main' (Line 18) ---")

    try:
        builder = ExtendedCallGraphBuilder(c_code, start_line=18)

        step_count = 1
        print("--- Traversing Bottom-Up ---")
        while True:
            node = builder.next()
            if node is None:
                break

            print(f"\n[Step {step_count}] Visiting: {node}")

            annotated = builder.annotate_node(node)
            print(annotated)  # Uncomment to see full source

            step_count += 1

        print("\n--- Final Edges ---")
        for src, dst in builder.graph_edges:
            print(f"{src.name} -> {dst.name}")

    except Exception as e:
        print(f"Error: {e}")
import sys
import clang.cindex
from collections import deque

# Configure clang path if necessary. 
# If you get a "library not found" error, uncomment and adjust the line below:
# make sure that the python binding version matches the llvm version. 
clang.cindex.Config.set_library_file('/usr/lib/llvm-14/lib/libclang.so')

class GraphNode:
    """
    Represents a node in the Extended Call Graph (either a Function or a Loop).
    """
    def __init__(self, cursor, node_type):
        self.cursor = cursor
        self.node_type = node_type  # "Function" or "Loop"
        # Generate a unique ID. Functions have USRs; Loops need a location-based ID.
        if node_type == "Function":
            self.id = cursor.get_usr()
            self.name = cursor.spelling
        else:
            loc = cursor.location
            self.id = f"Loop:{loc.file.name}:{loc.line}:{loc.column}"
            self.name = f"Loop at line {loc.line}"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"<{self.node_type}: {self.name}>"

    def get_extent(self):
        """Returns the start and end byte offsets of this node in the source file."""
        extent = self.cursor.extent
        return extent.start.offset, extent.end.offset

class ExtendedCallGraphBuilder:
    def __init__(self, source_code, start_line, filename="example.c"):
        self.source_code = source_code
        self.filename = filename
        self.index = clang.cindex.Index.create()
        
        # Parse the code into an AST
        self.tu = self.index.parse(self.filename, args=['-std=c11'], 
                                   unsaved_files=[(self.filename, self.source_code)])
        
        # Algorithm State
        self.graph_nodes = set()
        self.graph_edges = []
        self.worklist = deque()
        self.visited_ids = set()
        
        # Traversal State
        self.current_node = None
        self.traversal_queue = deque()
        
        # 1. Initialize Root (Lines 1-2 of Algorithm)
        start_cursor = self._find_function_at_line(start_line)
        if not start_cursor:
            raise ValueError(f"No function found covering line {start_line}")
            
        self.root_node = GraphNode(start_cursor, "Function")
        self._add_node(self.root_node)
        self.worklist.append(self.root_node)

        # 2. Build the entire graph immediately using the Worklist algorithm
        self._build_complete_graph()

        # 3. Compute Bottom-Up Order (Post-Order Traversal)
        self._compute_bottom_up_order()

    def _safe_get_children(self, cursor):
        """Safely iterate over children, skipping nodes that cause binding errors."""
        try:
            children_iter = iter(cursor.get_children())
        except ValueError:
            return

        while True:
            try:
                yield next(children_iter)
            except StopIteration:
                break
            except ValueError:
                continue
            except Exception:
                continue

    def _find_function_at_line(self, line):
        """Traverse AST to find the function definition surrounding a specific line."""
        found = None
        def visitor(cursor):
            nonlocal found
            if found: return
            try:
                if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL and cursor.is_definition():
                    start = cursor.extent.start.line
                    end = cursor.extent.end.line
                    if start <= line <= end:
                        found = cursor
                        return
            except ValueError:
                pass
            for child in self._safe_get_children(cursor):
                visitor(child)
        visitor(self.tu.cursor)
        return found

    def _add_node(self, node):
        if node.id not in self.visited_ids:
            self.graph_nodes.add(node)
            self.visited_ids.add(node.id)
            return True
        return False

    def _build_complete_graph(self):
        """Runs the Worklist algorithm until completion to build the full graph structure."""
        while self.worklist:
            # Line 4: Select and remove a node
            fn_node = self.worklist.popleft()
            # Line 5: Scan children
            self._scan_children(fn_node.cursor, fn_node)

    def _scan_children(self, parent_cursor, parent_node):
        """Scans for Calls and Loops, adding them to graph and worklist."""
        for child in self._safe_get_children(parent_cursor):
            try:
                # Line 6: If bb calls function M
                if child.kind == clang.cindex.CursorKind.CALL_EXPR:
                    target_def = child.get_definition()
                    if target_def:
                        target_node = GraphNode(target_def, "Function")
                        is_new = self._add_node(target_node)
                        self.graph_edges.append((parent_node, target_node))
                        if is_new:
                            self.worklist.append(target_node)

                # Line 11: If bb is a loop entry
                elif child.kind in (clang.cindex.CursorKind.FOR_STMT, 
                                    clang.cindex.CursorKind.WHILE_STMT, 
                                    clang.cindex.CursorKind.DO_STMT):
                    loop_node = GraphNode(child, "Loop")
                    is_new = self._add_node(loop_node)
                    self.graph_edges.append((parent_node, loop_node))
                    if is_new:
                        self.worklist.append(loop_node)
                    continue 

                # Recurse for nested statements
                self._scan_children(child, parent_node)
            except ValueError:
                continue

    def _compute_bottom_up_order(self):
        """
        Performs a Post-Order DFS traversal to create a bottom-up sequence.
        Result is stored in self.traversal_queue.
        """
        # Build adjacency list for traversal
        adj = {node: [] for node in self.graph_nodes}
        for src, dst in self.graph_edges:
            adj[src].append(dst)
            
        visited = set()
        
        def dfs(node):
            if node in visited: return
            visited.add(node)
            
            # Visit children first (Deepest nodes first)
            for child in adj[node]:
                dfs(child)
                
            # Add self after children (Post-Order)
            self.traversal_queue.append(node)
            
        # Start DFS from the initial root node
        dfs(self.root_node)

    def next(self):
        """
        Returns the next node in the Bottom-Up sequence.
        """
        if not self.traversal_queue:
            return None
        
        # Pop from the left (the first item added in post-order is the deepest leaf)
        self.current_node = self.traversal_queue.popleft()
        return self.current_node

    def get_annotated_source(self):
        """
        Returns the source code string with the Current Node wrapped in comments.
        """
        if not self.current_node:
            return self.source_code

        start_offset, end_offset = self.current_node.get_extent()
        
        # Prepare the wrappers
        prefix = f"\n/* >>> CURRENT NODE ({self.current_node.name}) START >>> */\n"
        suffix = f"\n/* <<< CURRENT NODE ({self.current_node.name}) END <<< */\n"

        src_bytes = self.source_code.encode('utf-8')
        before = src_bytes[:start_offset].decode('utf-8')
        target = src_bytes[start_offset:end_offset].decode('utf-8')
        after = src_bytes[end_offset:].decode('utf-8')
        
        return before + prefix + target + suffix + after

# ==========================================
# Example Usage
# ==========================================

if __name__ == "__main__":
    c_code = """
    #include <stdio.h>

    void leaf_function() {
        printf("I am a leaf\\n");
    }

    void helper() {
        leaf_function();
    }

    void process_data() {
        for (int i = 0; i < 5; i++) {
            helper();
        }
    }

    int main() {
        int x = 0;
        while (x < 3) {
            process_data();
            x++;
        }
        return 0;
    }
    """
    
    # Line 18 is inside main()
    print("--- Initializing Builder starting at 'main' (Line 18) ---")
    
    try:
        builder = ExtendedCallGraphBuilder(c_code, start_line=18)
        
        step_count = 1
        print("--- Traversing Bottom-Up ---")
        while True:
            node = builder.next()
            if node is None:
                break
                
            print(f"\n[Step {step_count}] Visiting: {node}")
            
            # This will verify the bottom-up order:
            # Expect: leaf_function -> helper -> Loop(process) -> process_data -> Loop(main) -> main
            
            annotated = builder.get_annotated_source()
            print(annotated) # Uncomment to see full source
            
            step_count += 1

        print("\n--- Final Edges ---")
        for src, dst in builder.graph_edges:
            print(f"{src.name} -> {dst.name}")
            
    except Exception as e:
        print(f"Error: {e}")