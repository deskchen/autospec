# AutoSpec

Automated Specification Generation for C Programs using LLMs and Frama-C verification.

## Overview

AutoSpec is a tool that automatically generates and verifies ACSL (ANSI/ISO C Specification Language) specifications for C programs. It combines:

- **Static Analysis**: Decompose C programs into verifiable components
- **LLM-based Generation**: Generate ACSL contracts / loop annotations via an LLM
- **Formal Verification**: Verify specifications using Frama-C's WP (Weakest Precondition) plugin
- **Iterative Refinement**: Strengthen or weaken specifications based on verification feedback

_**AutoSpec currently supports verification of the frama-c-problems benchmark suite, with x509-parser support planned for future releases.**_

## Installation

1. **Build the Docker image:**

```bash
docker build -t autospec:dev .
```

2. **Run the container:**

```bash
docker run -dit --name autospec --gpus all --network host -v $(pwd):/workspace autospec:dev

docker exec -it autospec /bin/bash
```

> [!NOTE]
> - The README assumes the repo is mounted at `/workspace` inside the container.

3. **Verify the installation:**

```bash
./scripts/run_frama_c_problems.sh
```

This will run verification on benchmarks in `benchmarks/frama-c-problems/ground-truth` to verify that Frama-C and AutoSpec are working correctly.

## Usage

### Running Ground Truth Benchmarks

```bash
# Run all benchmark categories
./scripts/run_frama_c_problems.sh
```

> [!NOTE]
> If you are not already inside the container shell, enter it first:
>
> ```bash
> docker exec -it autospec /bin/bash
> ```
> [!TIP]
> If `frama-c` is not found inside the container, run:
>
> ```bash
> opam init
> eval $(opam env)
> ```

Verify a single file (ground truth or your own C file):

```bash
python3 -m autospec.cli.main verify benchmarks/frama-c-problems/ground-truth/loops/1.c --verbose
```

### Custom Timeout

```bash
python3 -m autospec.cli.main verify file.c --timeout 120
```

### CLI Help

```bash
python3 -m autospec.cli.main --help
python3 -m autospec.cli.main verify --help
```

**Benchmark Suites:**

AutoSpec includes comprehensive benchmark suites for evaluation:

```bash
# Run all benchmarks (frama-c-problems + x509-parser)
./scripts/run_all_benchmarks.sh

# Run only frama-c-problems (~51 programs)
./scripts/run_all_benchmarks.sh -o frama-c

# Skip x509-parser for faster testing
./scripts/run_all_benchmarks.sh -s

# Test specific category
./scripts/run_frama_c_problems.sh loops
./scripts/run_frama_c_problems.sh arrays_and_loops -v

# Test x509-parser only
./scripts/run_x509_parser.sh
```

See [benchmarks/README.md](benchmarks/README.md) for detailed documentation.


### Adding New C Programs

1. Create a C file under `benchmarks/frama-c-problems/` (or anywhere you like).
2. Add ACSL annotations (preconditions, postconditions, loop invariants).
3. Verify with AutoSpec:

```bash
python3 -m autospec.cli.main verify benchmarks/frama-c-problems/your_file.c
```

### Example ACSL Annotation

```c
/*@
  @ requires n > 0;
  @ requires \valid_read(arr + (0..n-1));
  @ ensures \result >= arr[0];
  @ ensures \forall integer i; 0 <= i < n ==> \result >= arr[i];
  @*/
int array_max(int *arr, int n) {
    // ... implementation
}
```

## Configuration

Edit `autospec/config.py` to customize:

- `FRAMA_C_COMMAND`: Path to Frama-C executable
- `FRAMA_C_TIMEOUT`: Overall verification timeout (default: 60s)
- `FRAMA_C_WP_TIMEOUT`: Per-proof timeout (default: 10s)
- `LOG_LEVEL`: Logging verbosity

Or use environment variables:

```bash
export FRAMA_C_TIMEOUT=120
export FRAMA_C_WP_TIMEOUT=20
export VERBOSE=true
```

## Automated Spec Generation with vLLM

This is the core end-to-end workflow: **LLM → insert ACSL → verify**.

### 1) Start an OpenAI-compatible vLLM server

In a terminal **inside Docker** (or on the host if you prefer), start the model server:

```bash
python3 -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen3-32B \
  --port 8000 \
  --dtype auto
```

> [!NOTE]
> - `scripts/gen_specs.py` talks to an OpenAI-compatible Chat Completions endpoint.

### 2) Run generation (and verify)

In a second terminal **inside Docker**:

```bash
PYTHONPATH=/workspace python3 scripts/gen_specs.py \
  --input-dir benchmarks/frama-c-problems/test-inputs \
  --output-dir outputs/annotated \
  --model Qwen/Qwen3-32B \
  --endpoint http://localhost:8000/v1/chat/completions \
  --verify
```

Key details:
- The script recursively processes all `.c` files under `--input-dir`.
- It annotates one function/loop at a time by inserting a returned `/*@ ... */` block immediately before the target node.
- With `--verify`, it calls the AutoSpec verifier on each produced file.
- If verification fails, it automatically enters a **final feedback correction loop** (up to 3 attempts) where Frama-C/WP output is fed back to the LLM to repair **ACSL only**.


## Results

Below is a side-by-side comparison on **`benchmarks/frama-c-problems/test-inputs` (51 programs)**:

| Metric | AutoSpec (initial) | AutoSpec + final feedback loop |
|---|---:|---:|
| Programs passed | 21 | 24 |
| Programs failed | 30 | 27 |
| Pass rate | 41.2% | 47.1% |
| Visual | <progress value="21" max="51"></progress> | <progress value="24" max="51"></progress> |

**What is the “final feedback loop”?** After a failed verification run, we feed the Frama-C/WP error output back into the LLM and ask it to **repair ACSL only** (no C code changes), then re-verify.

> [!NOTE]
> If you want a complete per-program listing, run `scripts/verify_all_outputs.py` and save the output (e.g., `... > results.txt`).

### Per-program comparison (51 programs)

<details>
<summary>Click to expand</summary>

| Program | AutoSpec | + Final feedback |
|---|:---:|:---:|
| `arrays_and_loops/1.c` | PASS | FAIL |
| `arrays_and_loops/2.c` | FAIL | PASS |
| `arrays_and_loops/3.c` | PASS | PASS |
| `arrays_and_loops/4.c` | FAIL | FAIL |
| `arrays_and_loops/5.c` | FAIL | FAIL |
| `general_wp_problems/absolute_value.c` | PASS | PASS |
| `general_wp_problems/add.c` | PASS | PASS |
| `general_wp_problems/ani.c` | FAIL | FAIL |
| `general_wp_problems/diff.c` | PASS | PASS |
| `general_wp_problems/gcd.c` | PASS | PASS |
| `general_wp_problems/max_of_2.c` | PASS | PASS |
| `general_wp_problems/power.c` | FAIL | FAIL |
| `general_wp_problems/simple_interest.c` | PASS | PASS |
| `general_wp_problems/swap.c` | PASS | PASS |
| `general_wp_problems/triangle_angles.c` | FAIL | FAIL |
| `general_wp_problems/triangle_sides.c` | PASS | PASS |
| `general_wp_problems/wp1.c` | FAIL | FAIL |
| `immutable_arrays/array_sum.c` | FAIL | FAIL |
| `immutable_arrays/binary_search.c` | FAIL | FAIL |
| `immutable_arrays/check_evens_in_array.c` | PASS | PASS |
| `immutable_arrays/max.c` | FAIL | PASS |
| `immutable_arrays/occurences_of_x.c` | FAIL | FAIL |
| `immutable_arrays/sample.c` | FAIL | FAIL |
| `immutable_arrays/search.c` | PASS | PASS |
| `immutable_arrays/search_2.c` | PASS | PASS |
| `loops/1.c` | FAIL | FAIL |
| `loops/2.c` | FAIL | FAIL |
| `loops/3.c` | PASS | FAIL |
| `loops/4.c` | FAIL | PASS |
| `loops/fact.c` | FAIL | FAIL |
| `loops/mult.c` | FAIL | FAIL |
| `loops/sum_digits.c` | FAIL | FAIL |
| `loops/sum_even.c` | FAIL | FAIL |
| `miscellaneous/array_find.c` | PASS | PASS |
| `miscellaneous/array_max_advanced.c` | FAIL | FAIL |
| `miscellaneous/array_swap.c` | PASS | PASS |
| `miscellaneous/increment_arr.c` | FAIL | FAIL |
| `miscellaneous/max_of_2.c` | PASS | PASS |
| `more_arrays/equal_arrays.c` | FAIL | PASS |
| `more_arrays/replace_evens.c` | FAIL | FAIL |
| `more_arrays/reverse_array.c` | FAIL | FAIL |
| `mutable_arrays/array_double.c` | FAIL | FAIL |
| `mutable_arrays/bubble_sort.c` | FAIL | FAIL |
| `pointers/add_pointers.c` | FAIL | FAIL |
| `pointers/add_pointers_3_vars.c` | FAIL | FAIL |
| `pointers/div_rem.c` | PASS | PASS |
| `pointers/incr_a_by_b.c` | FAIL | PASS |
| `pointers/max_pointers.c` | PASS | PASS |
| `pointers/order_3.c` | FAIL | FAIL |
| `pointers/reset_1st.c` | PASS | PASS |
| `pointers/swap.c` | PASS | PASS |

</details>

## Understanding Verification Results

### VALID ✓
All proof obligations were successfully verified. The specifications are correct.

### INVALID ✗
Some proof obligations failed. The code may have bugs or specifications may be too strong.

### TIMEOUT ⏱
Verification took too long. Try increasing timeout or simplifying specifications.

### UNKNOWN ❓
Prover couldn't determine validity. May need stronger loop invariants or different proof strategy.

## Troubleshooting

### "Frama-C not found"

**Docker:** rebuild the image (use `--no-cache` if needed):

```bash
docker build --no-cache -t autospec:dev .
```

Then, inside the container shell, initialize opam and load the environment:

```bash
opam init
eval $(opam env)
which frama-c
```

**Local:** ensure Frama-C is in PATH:

```bash
eval $(opam env)
which frama-c
```

### Verification Times Out

Increase timeout:
```bash
python3 -m autospec.cli.main verify file.c --timeout 300
```

### Import Errors

**Docker:** Make sure to mount the current directory:
```bash
docker run -v $(pwd):/workspace autospec:dev ...
```

**Local:** Run from project root and ensure Python can find the package:
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
# Run a specific category
./scripts/run_frama_c_problems.sh loops
./scripts/run_frama_c_problems.sh arrays_and_loops -v
```

### "Output directory not found" (verify scripts)

If you see `Output directory not found: outputs/...`, it’s almost always one of:
- **Wrong folder name** (e.g., missing an underscore like `annotated_correction_6`).
- **Wrong working directory**: relative paths are resolved from where you run the script.

Example:

```bash
# From repo root (inside Docker):
PYTHONPATH=/workspace python3 scripts/verify_all_outputs.py --output-dir outputs/annotated_correction_6

# From ./scripts:
PYTHONPATH=/workspace python3 verify_all_outputs.py --output-dir ../outputs/annotated_correction_6
```