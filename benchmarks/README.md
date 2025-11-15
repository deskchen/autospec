# AutoSpec Benchmarks

This directory contains benchmark programs for testing AutoSpec's specification generation and verification capabilities.

## Structure

- `frama_c_problems/`: Collection of C programs with ACSL annotations for verification with Frama-C

## Frama-C Problems

The `frama_c_problems/` directory contains sample C programs annotated with ACSL specifications. These programs test various verification scenarios:

- Array bounds checking
- Null pointer validation
- Integer overflow detection
- Loop invariants
- Function contracts

### Included Samples

1. **array_max.c**: Find maximum element in an array with proper bounds checking
2. **binary_search.c**: Binary search with loop invariants
3. **abs_value.c**: Absolute value function with overflow handling

## Adding More Benchmarks

To add benchmarks from the Frama-C repository or other sources:

```bash
# Clone Frama-C examples
cd benchmarks/frama_c_problems
git clone https://github.com/Frama-C/Frama-C-snapshot.git frama-c-examples
# Or manually download specific examples

# For SyGuS benchmarks:
# Visit https://sygus.org/ and download invariant synthesis benchmarks
```

## Usage

Run verification on a benchmark:

```bash
python3 -m autospec.cli.main verify benchmarks/frama_c_problems/array_max.c
```

Or with Docker:

```bash
docker run -v $(pwd):/workspace autospec python3 -m autospec.cli.main verify benchmarks/frama_c_problems/array_max.c
```

