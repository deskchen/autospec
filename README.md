# AutoSpec

Automated Specification Generation for C Programs using LLMs and Frama-C verification.

## Overview

AutoSpec is a tool that automatically generates and verifies ACSL (ANSI/ISO C Specification Language) specifications for C programs. It combines:

- **Static Analysis**: Decompose C programs into verifiable components
- **LLM-based Generation**: Generate specifications using language models (placeholder for local models)
- **Formal Verification**: Verify specifications using Frama-C's WP (Weakest Precondition) plugin
- **Iterative Refinement**: Strengthen or weaken specifications based on verification feedback


## Installation

### Docker Setup (Recommended)

1. **Build the Docker image:**

```bash
docker build -t autospec:dev .
```

This will:
- Install OPAM and Frama-C
- Set up Python environment
- Install all dependencies

2. **Verify the installation:**

```bash
docker run autospec:dev frama-c -version
```

### Local Installation

1. **Install OPAM and Frama-C:**

```bash
# Install OPAM
sudo apt-get install opam

# Initialize OPAM
opam init
eval $(opam env)

# Install Frama-C
opam install frama-c
```

2. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

3. **Verify installation:**

```bash
frama-c -version
python3 -m autospec.cli.main --version
```

## Benchmark Preparation

The repository includes 3 sample C programs with ACSL annotations in `benchmarks/frama_c_problems/`:

- `array_max.c` - Find maximum in array with bounds checking
- `binary_search.c` - Binary search with loop invariants
- `abs_value.c` - Absolute value with overflow handling

### Download Additional Benchmarks

Run the preparation script:

```bash
./scripts/prepare_benchmarks.sh
```

Or manually download benchmarks:

**Frama-C Examples:**
```bash
cd benchmarks/frama_c_problems
git clone https://github.com/Frama-C/Frama-C-snapshot.git frama-c-examples
```

**SyGuS Benchmarks:**
1. Visit https://sygus.org/
2. Download invariant synthesis track benchmarks
3. Extract to `benchmarks/sygus/`

## Usage

### Basic Verification

**With Docker:**

```bash
docker run -dit --name autospec --gpus all -v $(pwd):/workspace autospec:dev

docker exec -it autospec /bin/bash

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

docker exec -it autospec /bin/bash

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
```

## Automated Spec Generation with vLLM

This repo includes a driver that iteratively generates ACSL specs via a local, OpenAI-compatible vLLM server and then verifies them.

### Start a local vLLM server

```bash
CUDA_VISIBLE_DEVICES=3 python3 -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen3-32B \
  --port 8000 --dtype auto --gpu-memory-utilization 0.80
```

### Generate specs (iterative, per CURRENT NODE)

```bash
python3 scripts/gen_specs.py \
  --input-dir benchmarks/frama-c-problems/test-inputs \
  --output-dir outputs/annotated \
  --model Qwen/Qwen3-32B \
  --endpoint http://localhost:8000/v1/chat/completions \
  --verify             # optional: run autospec verification after generation
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

## LLM Prompt for ACSL Specification Generation

The following few-shot prompt can be used to instruct an LLM to generate ACSL specifications **only for a designated region** of a C program.  
The designated region is marked using comments inserted by the extended call-graph tool:

```c
/* >>> CURRENT NODE (<name>) START >>> */
// ... code for the current function or loop ...
/* <<< CURRENT NODE (<name>) END <<< */
```

The model must:
- **Only add specifications for the CURRENT NODE region**.
- **Not modify any code or add specs outside the CURRENT NODE region**.
- **Mimic the style of the ground-truth benchmarks** in `benchmarks/frama-c-problems/ground-truth/` (e.g., pointer validity, separation, assigns, ensures, loop invariants).

Below is a ready-to-use prompt (instructions + examples).

### Few-Shot Prompt

You can pass the following text as the LLM prompt; replace the final `NEW INPUT` block with the annotated source you want to process.

```text
You are a formal verification assistant for C programs using ACSL and Frama-C.

You are given a complete C file. Exactly one region is marked as the "CURRENT NODE" using comments of the form:

    /* >>> CURRENT NODE (<name>) START >>> */
    ... C code for a single function or loop ...
    /* <<< CURRENT NODE (<name>) END <<< */

Your task:
- Write ACSL specifications **only for the CURRENT NODE region**.
- Do **not** add or change code or specifications outside the CURRENT NODE comments.
- Preserve all existing code and formatting (you see it for context, but you will not rewrite it).
- Use ACSL style consistent with the ground-truth examples (preconditions, assigns, postconditions, loop invariants, variants, etc.).

Rules:
1. If the CURRENT NODE is a **function**:
   - Generate a full ACSL contract that can be inserted immediately before the CURRENT NODE function.
   - Include `requires` clauses for pointer validity, separation, numeric ranges, and other necessary preconditions.
   - Include `assigns` describing the memory locations that may be modified.
   - Include `ensures` describing the functional behavior of the function.
2. If the CURRENT NODE is a **loop**:
   - Generate a `/*@ ... */` block containing at least:
     - `loop invariant` predicates,
     - `loop assigns` (if the loop writes to memory),
     - and, when appropriate, a `loop variant` that ensures termination.
   - This block will be inserted immediately before the loop header within the CURRENT NODE region by an external tool.
3. **Output format**: Output **only** the ACSL specification block as a `/*@ ... */` comment.  
   Do **not** output any C code, includes, or the CURRENT NODE delimiters.
4. Assume the delimiters remain in the source file; you do not need to output them or modify them.

---
EXAMPLE 1 — Function node with pointers

INPUT:

```c
#include <limits.h>

/* >>> CURRENT NODE (add) START >>> */
int add(int *a, int *b, int *r) {
    return *a + *b + *r;
}
/* <<< CURRENT NODE (add) END <<< */

int main() {
    int a = 24;
    int b = 32;
    int r = 12;
    int x;

    x = add(&a, &b, &r);
    //@ assert x == a + b + r;
    //@ assert x == 68;

    x = add(&a, &a, &a);
    //@ assert x == a + a + a;
    //@ assert x == 72;
}
```

OUTPUT:

```c
/*@
    requires \valid_read(a) && \valid_read(b) && \valid_read(r);
    // Preconditions to prevent overflow
    requires *a + *b + *r <= INT_MAX;
    requires *a + *b + *r >= INT_MIN;
    assigns \nothing;
    ensures \result == *a + *b + *r;
*/
```

---
EXAMPLE 2 — Loop node in `main`

INPUT:

```c
#include <stdio.h>

void leaf_function() {
    printf("I am a leaf\n");
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

    /* >>> CURRENT NODE (Loop at line 20) START >>> */
    while (x < 3) {
        process_data();
        x++;
    }
    /* <<< CURRENT NODE (Loop at line 20) END <<< */

    return 0;
}
```

OUTPUT:

```c
/*@
    loop invariant 0 <= x <= 3;
    loop assigns x;
    loop variant 3 - x;
*/
```

---
NEW INPUT:

Now follow the same pattern for the next CURRENT NODE. Here is the C file you must annotate:

```c
<paste the full C file here, including exactly one CURRENT NODE region>
```
```


