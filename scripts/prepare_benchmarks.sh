#!/bin/bash
# Script to download and prepare additional benchmark programs

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BENCHMARKS_DIR="$PROJECT_ROOT/benchmarks"
FRAMA_C_DIR="$BENCHMARKS_DIR/frama_c_problems"

echo "=== AutoSpec Benchmark Preparation ==="
echo "Benchmarks directory: $BENCHMARKS_DIR"
echo ""

# Ensure directories exist
mkdir -p "$FRAMA_C_DIR"

echo "✓ Basic benchmark structure created"
echo ""
echo "Sample benchmarks are already included in benchmarks/frama_c_problems/:"
ls -1 "$FRAMA_C_DIR"/*.c 2>/dev/null || echo "  (no .c files found - run from project root)"
echo ""

# Download additional Frama-C examples (optional)
echo "To download additional Frama-C benchmarks:"
echo "  1. Visit https://git.frama-c.com/pub/frama-c"
echo "  2. Or clone specific examples:"
echo "     git clone https://github.com/Frama-C/Frama-C-snapshot.git $FRAMA_C_DIR/frama-c-examples"
echo ""

# Download SyGuS benchmarks (optional)
echo "To download SyGuS invariant synthesis benchmarks:"
echo "  1. Visit https://sygus.org/"
echo "  2. Download the invariant track benchmarks"
echo "  3. Extract to $BENCHMARKS_DIR/sygus/"
echo ""

echo "=== Preparation Complete ==="
echo ""
echo "You can now run verification on the sample benchmarks:"
echo "  python3 -m autospec.cli.main verify benchmarks/frama_c_problems/array_max.c"
echo ""
echo "Or with Docker:"
echo "  docker run -v \$(pwd):/workspace autospec python3 -m autospec.cli.main verify benchmarks/frama_c_problems/array_max.c"

