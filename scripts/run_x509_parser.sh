#!/bin/bash
# Script to run Frama-C verification on x509-parser benchmark

# Don't exit on error - we handle verification failures ourselves
set +e

# Ensure OPAM environment is loaded (for Docker container)
if command -v opam &> /dev/null; then
    eval $(opam env) 2>/dev/null || true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
X509_DIR="$PROJECT_ROOT/benchmarks/x509-parser"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Run Frama-C verification on x509-parser benchmark"
    echo ""
    echo "Options:"
    echo "  -c, --clean     Clean build artifacts before running"
    echo "  -v, --verbose   Show detailed output"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0              # Run verification"
    echo "  $0 -c           # Clean and run verification"
    echo "  $0 -v           # Run with verbose output"
}

# Parse arguments
CLEAN=0
VERBOSE=0

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -c|--clean)
            CLEAN=1
            shift
            ;;
        -v|--verbose)
            VERBOSE=1
            shift
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

echo "=== AutoSpec X.509 Parser Benchmark Runner ==="
echo "X.509 directory: $X509_DIR"
echo ""

# Check if x509-parser directory exists
if [[ ! -d "$X509_DIR" ]]; then
    echo -e "${RED}ERROR: x509-parser directory not found at $X509_DIR${NC}"
    exit 1
fi

# Check if Makefile exists
if [[ ! -f "$X509_DIR/Makefile" ]]; then
    echo -e "${RED}ERROR: Makefile not found in $X509_DIR${NC}"
    exit 1
fi

cd "$X509_DIR"

# Clean if requested
if [[ $CLEAN -eq 1 ]]; then
    echo "Cleaning previous build artifacts..."
    make clean 2>&1 || true
    echo ""
fi

# Run Frama-C verification
echo "Running Frama-C verification on x509-parser..."
echo "This may take several minutes..."
echo ""

if [[ $VERBOSE -eq 1 ]]; then
    # Show full output
    if make frama-c; then
        echo ""
        echo -e "${GREEN}✓ X.509 Parser verification PASSED${NC}"
        exit 0
    else
        echo ""
        echo -e "${RED}✗ X.509 Parser verification FAILED${NC}"
        exit 1
    fi
else
    # Capture output and show summary
    if output=$(make frama-c 2>&1); then
        echo "$output" | tail -20
        echo ""
        echo -e "${GREEN}✓ X.509 Parser verification PASSED${NC}"
        exit 0
    else
        echo "$output" | tail -30
        echo ""
        echo -e "${RED}✗ X.509 Parser verification FAILED${NC}"
        echo ""
        echo "Run with -v flag for full output"
        exit 1
    fi
fi

