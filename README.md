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
docker run autospec frama-c -version
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
docker run -dit --name autospec -v $(pwd):/workspace autospec:dev

docker exec -it autospec /bin/bash

python3 -m autospec.cli.main verify benchmarks/frama-c-problems/loops/1.c --verbose
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
```

