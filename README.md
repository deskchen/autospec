# AutoSpec

Automated Specification Generation for C Programs using LLMs and Frama-C verification.

## Overview

AutoSpec is a tool that automatically generates and verifies ACSL (ANSI/ISO C Specification Language) specifications for C programs. It combines:

- **Static Analysis**: Decompose C programs into verifiable components
- **LLM-based Generation**: Generate specifications using language models (placeholder for local models)
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

docker exec -it autospec /bin/bash



opam init
eval $(opam env)


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

1. Create a C file in `benchmarks/frama_c_problems/`
2. Add ACSL annotations (preconditions, postconditions, loop invariants)
3. Verify with AutoSpec:

```bash
python3 -m autospec.cli.main verify benchmarks/frama_c_problems/your_file.c
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

**Docker:** Rebuild the image:
```bash
docker build --no-cache -t autospec:dev .


```

**Local:** Ensure Frama-C is in PATH:
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

## Automated Spec Generation with vLLM

```bash
# (Terminal 1 inside docker)
python3 -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen3-32B \
  --port 8000 --dtype auto 
```

```bash
source .venv/bin/activate


PYTHONPATH=/workspace python3 scripts/gen_specs.py \


# (Terminal 2 inside docker)
python3 scripts/gen_specs.py \
  --input-dir benchmarks/frama-c-problems/test-inputs \
  --output-dir outputs/annotated \
  --model Qwen/Qwen3-32B \
  --endpoint http://localhost:8000/v1/chat/completions \
  --verify      
```

Key details:
- The script recursively processes all `.c` files under `--input-dir` (default: `benchmarks/frama-c-problems/test-inputs`).
- For each function/loop (CURRENT NODE), it:
  1. Wraps the node with CURRENT NODE markers.
  2. Sends the full file + markers + accumulated specs to the LLM using the README few-shot prompt.
  3. Inserts the returned ACSL block immediately before the target node.
  4. Repeats until all nodes have specs, writes to `--output-dir` (default: `outputs/annotated`).
- `--verify` runs `python3 -m autospec.cli.main verify <annotated-file> --verbose --timeout 120`.
- Configure endpoint/auth via:
  - `--endpoint` (default: `http://localhost:8000/v1/chat/completions`)
  - `--model` (default: `Qwen/Qwen3-32B`)
  - `OPENAI_API_KEY` (optional; sent as Bearer)

## Configuration

Edit `autospec/config.py` to customize:

- `FRAMA_C_COMMAND`: Path to Frama-C executable
- `FRAMA_C_TIMEOUT`: Overall verification timeout (default: 60s)
- `FRAMA_C_WP_TIMEOUT`: Per-proof timeout (default: 10s)
- `LOG_LEVEL`: Logging verbosity


## Troubleshooting

### "Frama-C not found"

```bash
eval $(opam env) # Run this manually inside the docker
```


original result:
```
Program Success
arrays_and_loops/1.c    PASS
arrays_and_loops/2.c    FAIL
arrays_and_loops/3.c    PASS
arrays_and_loops/4.c    FAIL
arrays_and_loops/5.c    FAIL
general_wp_problems/absolute_value.c    PASS
general_wp_problems/add.c       PASS
general_wp_problems/ani.c       FAIL
general_wp_problems/diff.c      PASS
general_wp_problems/gcd.c       PASS
general_wp_problems/max_of_2.c  PASS
general_wp_problems/power.c     FAIL
general_wp_problems/simple_interest.c   PASS
general_wp_problems/swap.c      PASS
general_wp_problems/triangle_angles.c   FAIL
general_wp_problems/triangle_sides.c    PASS
general_wp_problems/wp1.c       FAIL
immutable_arrays/array_sum.c    FAIL
immutable_arrays/binary_search.c        FAIL
immutable_arrays/check_evens_in_array.c PASS
immutable_arrays/max.c  FAIL
immutable_arrays/occurences_of_x.c      FAIL
immutable_arrays/sample.c       FAIL
immutable_arrays/search.c       PASS
immutable_arrays/search_2.c     PASS
loops/1.c       FAIL
loops/2.c       FAIL
loops/3.c       PASS
loops/4.c       FAIL
loops/fact.c    FAIL
loops/mult.c    FAIL
loops/sum_digits.c      FAIL
loops/sum_even.c        FAIL
miscellaneous/array_find.c      PASS
miscellaneous/array_max_advanced.c      FAIL
miscellaneous/array_swap.c      PASS
miscellaneous/increment_arr.c   FAIL
miscellaneous/max_of_2.c        PASS
more_arrays/equal_arrays.c      FAIL
more_arrays/replace_evens.c     FAIL
more_arrays/reverse_array.c     FAIL
mutable_arrays/array_double.c   FAIL
mutable_arrays/bubble_sort.c    FAIL
pointers/add_pointers.c FAIL
pointers/add_pointers_3_vars.c  FAIL
pointers/div_rem.c      PASS
pointers/incr_a_by_b.c  FAIL
pointers/max_pointers.c PASS
pointers/order_3.c      FAIL
pointers/reset_1st.c    PASS
pointers/swap.c PASS

Summary: 21/51 passed
```