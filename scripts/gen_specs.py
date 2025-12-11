#!/usr/bin/env python3
"""
Iteratively generate ACSL specifications using a vLLM (OpenAI-compatible) endpoint.

Workflow:
1) Decompose each C file into a bottom-up sequence of functions/loops (ExtendedCallGraphBuilder).
2) For the next node that lacks a preceding ACSL block, wrap it with CURRENT NODE markers,
   build the few-shot prompt (from README), and call the LLM.
3) Insert the returned ACSL block immediately before the target node.
4) Repeat until all nodes are annotated, then optionally verify with AutoSpec CLI.
"""

import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import Optional

import requests

from autospec.decomposition import ExtendedCallGraphBuilder, GraphNode

# Few-shot prompt body (mirrors README instructions)
FEWSHOT_PROMPT = """You are a formal verification assistant for C programs using ACSL and Frama-C.

You are given a complete C file. Exactly one region is marked as the "CURRENT NODE" using comments of the form:

    /* >>> CURRENT NODE (<name>) START >>> */
    ... C code for a single function or loop ...
    /* <<< CURRENT NODE (<name>) END <<< */

Your task:
- Write ACSL specifications only for the CURRENT NODE region.
- Do not add or change code or specifications outside the CURRENT NODE comments.
- Preserve all existing code and formatting (you see it for context, but you will not rewrite it).
- Use ACSL style consistent with the ground-truth examples (preconditions, assigns, postconditions, loop invariants, variants, etc.).

Rules:
1. If the CURRENT NODE is a function:
   - Generate a full ACSL contract that can be inserted immediately before the CURRENT NODE function.
   - Include requires clauses for pointer validity, separation, numeric ranges, and other necessary preconditions.
   - Include assigns describing the memory locations that may be modified.
   - Include ensures describing the functional behavior of the function.
2. If the CURRENT NODE is a loop:
   - Generate a /*@ ... */ block containing at least:
     - loop invariant predicates,
     - loop assigns (if the loop writes to memory),
     - and, when appropriate, a loop variant that ensures termination.
   - This block will be inserted immediately before the loop header within the CURRENT NODE region by an external tool.
3. Output format: Output only the ACSL specification block as a /*@ ... */ comment.
   Do not output any C code, includes, the CURRENT NODE delimiters, or any natural language explanation.
   Do NOT output any <think> blocks, reasoning text, or commentary; only a single /*@ ... */ block.
4. Assume the delimiters remain in the source file; you do not need to output or modify them.

Example output for a function node:
/*@
    requires \\valid_read(a) && \\valid_read(b) && \\valid_read(r);
    requires *a + *b + *r <= INT_MAX;
    requires *a + *b + *r >= INT_MIN;
    assigns \\nothing;
    ensures \\result == *a + *b + *r;
*/

Example output for a loop node:
/*@
    loop invariant 0 <= x <= 3;
    loop assigns x;
    loop variant 3 - x;
*/
"""


def discover_c_files(root: Path):
    return sorted(p for p in root.rglob("*.c") if p.is_file())


def has_preceding_spec(src: str, node: GraphNode, window: int = 800) -> bool:
    start_offset, _ = node.get_extent()
    snippet = src[max(0, start_offset - window) : start_offset]
    return bool(re.search(r"/\*@[\s\S]*?\*/\s*$", snippet))


def indent_block(block: str, indent: str) -> str:
    lines = block.strip().splitlines()
    return "\n".join(indent + line for line in lines)


def insert_spec(src: str, node: GraphNode, spec_block: str) -> str:
    start_offset, _ = node.get_extent()
    line_start = src.rfind("\n", 0, start_offset)
    line_start = 0 if line_start == -1 else line_start + 1
    indent = src[line_start:start_offset]
    spec_text = indent_block(spec_block.strip(), indent)

    # Ensure a leading newline before the spec if needed
    prefix = "" if start_offset == 0 or src[start_offset - 1] == "\n" else "\n"
    insertion = f"{prefix}{spec_text}\n"
    return src[:start_offset] + insertion + src[start_offset:]


def build_prompt(code_with_marker: str) -> str:
    return f"{FEWSHOT_PROMPT}\n\nHere is the C file to annotate:\n```c\n{code_with_marker}\n``` /nothink"


def call_llm(prompt: str, endpoint: str, model: str, temperature: float, max_tokens: int, api_key: Optional[str]) -> str:
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You produce ACSL specifications only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    # Debug: show outbound request metadata and only the C code to be annotated
    # (avoid dumping the full prompt with instructions).
    print("\n[DEBUG] LLM request:")
    print(f"  endpoint={endpoint}")
    print(f"  model={model}")
    print(f"  temperature={temperature}")
    print(f"  max_tokens={max_tokens}")
    print(f"  prompt_chars={len(prompt)}")
    # Try to extract just the C code snippet between ```c ... ```.
    code_snippet = None
    match = re.search(r"```c\n([\s\S]*?)\n```", prompt)
    if match:
        code_snippet = match.group(1)
    print("  C code to annotate:")
    if code_snippet:
        print(code_snippet)
    else:
        print("  [DEBUG] C code snippet not found in prompt.")

    resp = requests.post(endpoint, headers=headers, json=payload, timeout=120)
    print(f"[DEBUG] LLM response status: {resp.status_code}")
    print("[DEBUG] LLM raw response text:")
    print(resp.text)

    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"]


def extract_spec_block(text: str) -> Optional[str]:
    """
    Extract the first ACSL spec block of the form /*@ ... */.

    If none is found, return None instead of treating arbitrary text as a spec.
    This prevents accidentally inserting LLM reasoning or other non-ACSL content
    into the C source, which would break parsing.
    """
    match = re.search(r"/\*@[\s\S]*?\*/", text)
    if match:
        return match.group(0)

    # Debug: show that we failed to find a spec block.
    cleaned = text.strip()
    if cleaned:
        print("[DEBUG] No ACSL /*@ ... */ block found in LLM output. Raw content:")
        # Truncate to avoid spamming logs on very long responses.
        preview = cleaned if len(cleaned) <= 2000 else cleaned[:2000] + "\n...[truncated]..."
        print(preview)
    return None


def annotate_file(path: Path, args) -> Path:
    src = path.read_text()
    api_key = os.getenv("OPENAI_API_KEY")

    while True:
        builder = ExtendedCallGraphBuilder(src, start_line=None, filename=str(path))
        nodes_order = list(builder.traversal_queue)
        target = None
        for node in nodes_order:
            if has_preceding_spec(src, node):
                continue
            target = node
            break

        if not target:
            break

        marked = builder.annotate_node(target)
        prompt = build_prompt(marked)
        llm_raw = call_llm(prompt, args.endpoint, args.model, args.temperature, args.max_tokens, api_key)
        spec_block = extract_spec_block(llm_raw)
        if not spec_block:
            raise RuntimeError(f"LLM did not return a spec for {path} / node {target.name}")

        src = insert_spec(src, target, spec_block)

    rel = path.relative_to(args.input_dir)
    out_path = args.output_dir / rel
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(src)
    return out_path


def setup_opam_environment():
    """
    Set up OPAM environment to ensure frama-c is in PATH.
    Equivalent to: eval $(opam env)
    Note: Even though PATH is set in Dockerfile, we need to run opam env to actually load it.
    """
    # Run 'opam env' and apply its output to current process environment
    try:
        result = subprocess.run(
            ["opam", "env"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
            env=os.environ.copy()  # Pass current environment to subprocess
        )
        if result.returncode == 0:
            # Parse opam env output (format: VAR='value'; export VAR;)
            for line in result.stdout.splitlines():
                line = line.strip()
                # Handle: VAR='value'; export VAR;
                # Match pattern like: PATH='/home/opam/.opam/4.14/bin:$PATH'; export PATH;
                match = re.match(r"(\w+)='([^']+)';\s*export\s+\w+;", line)
                if match:
                    var_name, var_value = match.groups()
                    # Expand $VAR references using current environment
                    var_value = os.path.expandvars(var_value)
                    os.environ[var_name] = var_value
    except (FileNotFoundError, subprocess.TimeoutExpired):
        # opam command not found or timed out, that's okay
        # PATH is already set in Dockerfile, so frama-c should still be available
        pass


def run_verify(out_path: Path, timeout: int):
    # Ensure opam environment is set up before verification
    setup_opam_environment()
    
    cmd = [
        "python3",
        "-m",
        "autospec.cli.main",
        "verify",
        str(out_path),
        "--timeout",
        str(timeout),
        "--verbose",
    ]
    return subprocess.run(cmd, capture_output=True, text=True, check=False)


def main():
    # Set up OPAM environment early to ensure frama-c is available
    setup_opam_environment()
    
    parser = argparse.ArgumentParser(description="Generate ACSL specs via vLLM (OpenAI-compatible).")
    parser.add_argument("--input-dir", type=Path, default=Path("benchmarks/frama-c-problems/test-inputs/arrays_and_loops"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/annotated"))
    parser.add_argument("--endpoint", type=str, default="http://localhost:8000/v1/chat/completions")
    parser.add_argument("--model", type=str, default="Qwen/Qwen3-32B")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--max-tokens", type=int, default=512)
    parser.add_argument("--verify", action="store_true", help="Run autospec verify after annotation.")
    parser.add_argument("--verify-timeout", type=int, default=120, help="Timeout for verification (seconds).")
    args = parser.parse_args()

    files = discover_c_files(args.input_dir)
    if not files:
        raise SystemExit(f"No C files found under {args.input_dir}")

    print(f"Found {len(files)} C files under {args.input_dir}")
    for path in files:
        print(f"\n[Annotate] {path}")
        out_path = annotate_file(path, args)
        print(f" -> wrote {out_path}")
        if args.verify:
            result = run_verify(out_path, args.verify_timeout)
            print(f" -> verify exit={result.returncode}")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)


if __name__ == "__main__":
    main()

