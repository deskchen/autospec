# AutoSpec Benchmarks

This directory contains benchmark programs for testing AutoSpec's specification generation and verification capabilities.

## Benchmark Suites

### 1. frama-c-problems
Collection of C programs organized by problem type, sourced from educational Frama-C exercises.

**Categories:**
- `arrays_and_loops/` - Array operations with loop invariants (5 programs)
- `general_wp_problems/` - General weakest precondition problems (12 programs)
- `immutable_arrays/` - Read-only array operations (8 programs)
- `loops/` - Loop verification challenges (8 programs)
- `miscellaneous/` - Mixed verification problems (5 programs)
- `more_arrays/` - Additional array manipulation (3 programs)
- `mutable_arrays/` - Array modification operations (2 programs)
- `pointers/` - Pointer manipulation and verification (8 programs)

**Total:** ~51 C programs

### 2. x509-parser
X.509 certificate parser with ACSL annotations, a real-world verification project.

**Source:** Production-grade C code from French cybersecurity agency (ANSSI)  
**Complexity:** Advanced - includes pointer arithmetic, memory management, complex data structures

## Running Benchmarks

### Quick Start

```bash
# Run all benchmarks
./scripts/run_all_benchmarks.sh

# Run only frama-c-problems
./scripts/run_all_benchmarks.sh -o frama-c

# Run with verbose output
./scripts/run_all_benchmarks.sh -v
```

### Testing Specific Categories

```bash
# Test a specific category from frama-c-problems
./scripts/run_frama_c_problems.sh loops

# Test with verbose output
./scripts/run_frama_c_problems.sh arrays_and_loops -v

# Test all frama-c categories
./scripts/run_frama_c_problems.sh
```

### Testing x509-parser

```bash
# Run x509-parser verification
./scripts/run_x509_parser.sh

# Clean and run
./scripts/run_x509_parser.sh -c

# Verbose output
./scripts/run_x509_parser.sh -v
```

## Script Options

### run_all_benchmarks.sh
```
Options:
  -v, --verbose        Show detailed output
  -s, --skip-x509      Skip x509-parser (faster testing)
  -o, --only SUITE     Run only 'frama-c' or 'x509'
  -h, --help           Show help
```

### run_frama_c_problems.sh
```
Usage: ./scripts/run_frama_c_problems.sh [CATEGORY] [OPTIONS]

Arguments:
  CATEGORY    Category to test (optional, tests all if not specified)

Options:
  -v, --verbose   Show detailed Frama-C output
  -h, --help      Show help
```

### run_x509_parser.sh
```
Options:
  -c, --clean     Clean build artifacts before running
  -v, --verbose   Show detailed output
  -h, --help      Show help
```

## Docker Usage

Run benchmarks inside the Docker container:

```bash
# Start interactive shell
docker run -it -v $(pwd):/workspace autospec /bin/bash

# Inside container, run benchmarks
./scripts/run_all_benchmarks.sh
./scripts/run_frama_c_problems.sh loops
./scripts/run_x509_parser.sh
```

Or run directly:

```bash
docker run -v $(pwd):/workspace autospec ./scripts/run_all_benchmarks.sh
```

## Expected Results

### frama-c-problems
- **Easy categories:** `general_wp_problems`, `immutable_arrays` - Most should verify (VALID)
- **Medium categories:** `loops`, `arrays_and_loops` - May have timeouts on complex invariants
- **Hard categories:** `mutable_arrays`, `pointers` - Some may be incomplete or timeout

### x509-parser
- Large, real-world code - expect several minutes to run
- Some proofs may timeout (this is expected for complex real-world code)
- Success means no invalid proofs, timeouts are acceptable

## Benchmark Statistics

Run benchmarks to see detailed statistics:

```bash
./scripts/run_frama_c_problems.sh

# Output includes:
# Total tests:    51
# Passed (VALID): XX
# Failed (INVALID): XX
# Timeout:        XX
# Unknown:        XX
# Success rate: XX%
```

## Adding Custom Benchmarks

1. **Add to existing category:**
   ```bash
   # Add your .c file to appropriate directory
   cp my_program.c benchmarks/frama-c-problems/loops/
   
   # Scripts will automatically pick it up
   ./scripts/run_frama_c_problems.sh loops
   ```

2. **Create new category:**
   ```bash
   mkdir benchmarks/frama-c-problems/my_category
   cp *.c benchmarks/frama-c-problems/my_category/
   
   # Update the CATEGORIES array in run_frama_c_problems.sh
   ```

## Troubleshooting

### "Frama-C not found"
Ensure you're running inside the Docker container or have Frama-C installed locally.

### Timeouts
Increase the timeout in `autospec/config.py`:
```python
FRAMA_C_WP_TIMEOUT = int(os.getenv("FRAMA_C_WP_TIMEOUT", "60"))
```

### x509-parser fails to build
Make sure you have all dependencies:
```bash
cd benchmarks/x509-parser
make clean
make
```

## Benchmark Sources

- **frama-c-problems:** Educational Frama-C repository
  - Repository: https://github.com/acsl-language/frama-c-problems
  - License: Educational use
  
- **x509-parser:** ANSSI X.509 Parser
  - Source: French cybersecurity agency (ANSSI)
  - License: Dual BSD/GPL v2
  - Original: https://github.com/ANSSI-FR/x509-parser

## Performance Notes

- **frama-c-problems:** ~2-5 minutes for all categories
- **x509-parser:** ~5-15 minutes (complex real-world code)
- **Full suite:** ~10-20 minutes total

Use `-s` flag to skip x509 for faster iteration during development:
```bash
./scripts/run_all_benchmarks.sh -s
```

## Verification Goals by Category

| Category | Total | Expected Valid | Expected Timeout | Notes |
|----------|-------|----------------|------------------|-------|
| general_wp_problems | 12 | 10-12 | 0-2 | Simple specifications |
| immutable_arrays | 8 | 7-8 | 0-1 | Array bounds checks |
| loops | 8 | 5-7 | 1-3 | Loop invariants can be complex |
| pointers | 8 | 6-8 | 0-2 | Pointer reasoning |
| arrays_and_loops | 5 | 3-5 | 0-2 | Combined complexity |
| mutable_arrays | 2 | 1-2 | 0-1 | Array modifications |
| more_arrays | 3 | 2-3 | 0-1 | Array operations |
| miscellaneous | 5 | 3-5 | 0-2 | Various topics |

## Next Steps

For the course project:
1. Run baseline benchmarks to establish current performance
2. Implement LLM-based specification generation
3. Add iterative refinement loop
4. Compare results with/without AutoSpec improvements
5. Document improvements in verification success rates

