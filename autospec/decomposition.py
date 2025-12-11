import clang.cindex
import os
from collections import deque
from typing import List, Optional, Tuple


def _find_clang_library():
    """
    Attempts to find the clang library by trying common installation paths.
    Falls back to letting clang find it automatically if none are found.
    """
    # Common paths to try (in order of preference)
    common_paths = [
        '/usr/lib/llvm-14/lib/libclang.so',
        '/usr/lib/llvm-18/lib/libclang.so',
        '/usr/lib/llvm-16/lib/libclang.so',
        '/usr/lib/llvm-15/lib/libclang.so',
        '/usr/lib/llvm-13/lib/libclang.so',
        '/usr/lib/x86_64-linux-gnu/libclang.so',
        '/usr/lib/x86_64-linux-gnu/libclang-18.so.18',
        '/usr/lib/x86_64-linux-gnu/libclang-14.so.1',
        '/usr/local/lib/libclang.so',
    ]
    
    # Also check environment variable
    env_path = os.getenv('LIBCLANG_PATH')
    if env_path and os.path.exists(env_path):
        try:
            clang.cindex.Config.set_library_file(env_path)
            return
        except Exception:
            pass
    
    # Try common paths
    for path in common_paths:
        if os.path.exists(path):
            try:
                clang.cindex.Config.set_library_file(path)
                return
            except Exception:
                continue
    
    # If no path found, let clang try to find it automatically
    # This will use the default search mechanism
    pass


# Configure clang path if necessary.
# If you get a "library not found" error, uncomment and adjust the line below:
# make sure that the python binding version matches the llvm version.
_find_clang_library()


class GraphNode:
    """
    Represents a node in the Extended Call Graph (either a Function or a Loop).
    """

    def __init__(self, cursor, node_type: str, parent_function_usr: Optional[str] = None):
        self.cursor = cursor
        self.node_type = node_type  # "Function" or "Loop"
        self.parent_function_usr = parent_function_usr
        if node_type == "Function":
            self.id = cursor.get_usr()
            self.name = cursor.spelling
        else:
            loc = cursor.location
            # Include parent function USR when available to make loop IDs more stable.
            parent = f"{parent_function_usr}:" if parent_function_usr else ""
            self.id = f"{parent}Loop:{loc.file.name}:{loc.line}:{loc.column}"
            self.name = f"Loop at line {loc.line}"

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return f"<{self.node_type}: {self.name}>"

    def get_extent(self) -> Tuple[int, int]:
        """Returns the start and end byte offsets of this node in the source file."""
        extent = self.cursor.extent
        return extent.start.offset, extent.end.offset


class ExtendedCallGraphBuilder:
    """
    Builds an extended call graph (functions + loops) and produces a bottom-up traversal order.
    """

    def __init__(self, source_code: str, start_line: Optional[int] = None, filename: str = "example.c"):
        self.source_code = source_code
        self.filename = filename
        self.index = clang.cindex.Index.create()

        self.tu = self.index.parse(
            self.filename,
            args=["-std=c11"],
            unsaved_files=[(self.filename, self.source_code)],
        )

        # Debug: surface libclang diagnostics early to help catch parse issues.
        if self.tu.diagnostics:
            print(f"[DEBUG] clang diagnostics for {self.filename}:")
            for diag in self.tu.diagnostics:
                print(f"  - {diag.severity}: {diag.spelling}")

        self.graph_nodes = set()
        self.graph_edges = []
        self.worklist = deque()
        self.visited_ids = set()
        self.current_node = None
        self.traversal_queue = deque()

        # Initialize root
        start_cursor = (
            self._find_function_at_line(start_line) if start_line is not None else self._find_first_function()
        )
        if not start_cursor:
            print(f"[DEBUG] No function found in {self.filename}.")
            print("[DEBUG] Source snippet (first 400 chars):")
            print(self.source_code[:400])
            # Show top-level cursor kinds to help debug AST shape.
            top_level = []
            for child in self._safe_get_children(self.tu.cursor):
                try:
                    top_level.append(child.kind)
                except Exception:
                    continue
            print(f"[DEBUG] Top-level cursor kinds: {top_level}")
            raise ValueError("No function found to initialize traversal.")

        self.root_node = GraphNode(start_cursor, "Function")
        self._add_node(self.root_node)
        self.worklist.append(self.root_node)

        # Build and compute order
        self._build_complete_graph()
        self._compute_bottom_up_order()

    # --------------------- internal helpers ---------------------
    def _safe_get_children(self, cursor):
        try:
            children_iter = iter(cursor.get_children())
        except ValueError:
            return
        while True:
            try:
                yield next(children_iter)
            except StopIteration:
                break
            except Exception:
                continue

    def _find_first_function(self):
        found = None

        def visitor(cursor):
            nonlocal found
            if found:
                return
            try:
                if cursor.kind == clang.cindex.CursorKind.FUNCTION_DECL and cursor.is_definition():
                    found = cursor
                    return
            except ValueError:
                pass
            for child in self._safe_get_children(cursor):
                visitor(child)

        visitor(self.tu.cursor)
        return found

    def _find_function_at_line(self, line: int):
        found = None

        def visitor(cursor):
            nonlocal found
            if found:
                return
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

    def _add_node(self, node: GraphNode):
        if node.id not in self.visited_ids:
            self.graph_nodes.add(node)
            self.visited_ids.add(node.id)
            return True
        return False

    def _build_complete_graph(self):
        while self.worklist:
            fn_node = self.worklist.popleft()
            self._scan_children(fn_node.cursor, fn_node)

    def _scan_children(self, parent_cursor, parent_node: GraphNode):
        parent_usr = parent_cursor.get_usr() if parent_cursor else None
        for child in self._safe_get_children(parent_cursor):
            try:
                if child.kind == clang.cindex.CursorKind.CALL_EXPR:
                    target_def = child.get_definition()
                    if target_def:
                        target_node = GraphNode(target_def, "Function")
                        is_new = self._add_node(target_node)
                        self.graph_edges.append((parent_node, target_node))
                        if is_new:
                            self.worklist.append(target_node)

                elif child.kind in (
                    clang.cindex.CursorKind.FOR_STMT,
                    clang.cindex.CursorKind.WHILE_STMT,
                    clang.cindex.CursorKind.DO_STMT,
                ):
                    loop_node = GraphNode(child, "Loop", parent_function_usr=parent_usr)
                    is_new = self._add_node(loop_node)
                    self.graph_edges.append((parent_node, loop_node))
                    if is_new:
                        self.worklist.append(loop_node)
                    continue

                self._scan_children(child, parent_node)
            except ValueError:
                continue

    def _compute_bottom_up_order(self):
        adj = {node: [] for node in self.graph_nodes}
        for src, dst in self.graph_edges:
            adj[src].append(dst)

        visited = set()

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for child in adj[node]:
                dfs(child)
            self.traversal_queue.append(node)

        dfs(self.root_node)

    # --------------------- public API ---------------------
    def next(self) -> Optional[GraphNode]:
        if not self.traversal_queue:
            return None
        self.current_node = self.traversal_queue.popleft()
        return self.current_node

    def nodes_bottom_up(self) -> List[GraphNode]:
        """Return nodes in bottom-up order without consuming the internal queue."""
        return list(self.traversal_queue)

    def annotate_current_node(self) -> str:
        """Annotate the source with markers for the current node."""
        if not self.current_node:
            return self.source_code
        return self.annotate_node(self.current_node)

    def annotate_node(self, node: GraphNode) -> str:
        """Return source with CURRENT NODE markers around the given node."""
        start_offset, end_offset = node.get_extent()
        prefix = f"\n/* >>> CURRENT NODE ({node.name}) START >>> */\n"
        suffix = f"\n/* <<< CURRENT NODE ({node.name}) END <<< */\n"

        src_bytes = self.source_code.encode("utf-8")
        before = src_bytes[: start_offset].decode("utf-8")
        target = src_bytes[start_offset:end_offset].decode("utf-8")
        after = src_bytes[end_offset:].decode("utf-8")
        return before + prefix + target + suffix + after


