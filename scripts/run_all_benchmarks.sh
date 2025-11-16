#!/bin/bash
# Master script to run all AutoSpec benchmarks

# Don't exit on error - we handle verification failures ourselves
set +e

# Ensure OPAM environment is loaded (for Docker container)
if command -v opam &> /dev/null; then
    eval $(opam env) 2>/dev/null || true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Run all AutoSpec benchmarks"
    echo ""
    echo "Options:"
    echo "  -v, --verbose        Show detailed output"
    echo "  -s, --skip-x509      Skip x509-parser benchmark (faster)"
    echo "  -o, --only SUITE     Run only specified suite (frama-c or x509)"
    echo "  -h, --help           Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                   # Run all benchmarks"
    echo "  $0 -v                # Run all with verbose output"
    echo "  $0 -s                # Skip x509-parser (faster)"
    echo "  $0 -o frama-c        # Run only frama-c-problems"
    echo "  $0 -o x509           # Run only x509-parser"
}

# Parse arguments
VERBOSE=""
SKIP_X509=0
ONLY_SUITE=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -v|--verbose)
            VERBOSE="-v"
            shift
            ;;
        -s|--skip-x509)
            SKIP_X509=1
            shift
            ;;
        -o|--only)
            ONLY_SUITE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit 1
            ;;
    esac
done

# Validate --only option
if [[ -n "$ONLY_SUITE" ]] && [[ "$ONLY_SUITE" != "frama-c" ]] && [[ "$ONLY_SUITE" != "x509" ]]; then
    echo "ERROR: Invalid suite '$ONLY_SUITE'. Must be 'frama-c' or 'x509'"
    exit 1
fi

# Track results
FRAMA_C_RESULT=0
X509_RESULT=0

echo "╔═══════════════════════════════════════════════════════╗"
echo "║   AutoSpec - Complete Benchmark Test Suite           ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

START_TIME=$(date +%s)

# Run frama-c-problems benchmarks
if [[ -z "$ONLY_SUITE" ]] || [[ "$ONLY_SUITE" == "frama-c" ]]; then
    echo -e "${BLUE}[1/2] Running frama-c-problems benchmarks...${NC}"
    echo ""
    
    if "$SCRIPT_DIR/run_frama_c_problems.sh" $VERBOSE; then
        FRAMA_C_RESULT=0
        echo ""
        echo -e "${GREEN}✓ frama-c-problems: PASSED${NC}"
    else
        FRAMA_C_RESULT=1
        echo ""
        echo -e "${RED}✗ frama-c-problems: FAILED${NC}"
    fi
    
    echo ""
    echo "───────────────────────────────────────────────────────"
    echo ""
fi

# Run x509-parser benchmark
if [[ -z "$ONLY_SUITE" ]] || [[ "$ONLY_SUITE" == "x509" ]]; then
    if [[ $SKIP_X509 -eq 0 ]]; then
        echo -e "${BLUE}[2/2] Running x509-parser benchmark...${NC}"
        echo ""
        
        if "$SCRIPT_DIR/run_x509_parser.sh" $VERBOSE; then
            X509_RESULT=0
            echo ""
            echo -e "${GREEN}✓ x509-parser: PASSED${NC}"
        else
            X509_RESULT=1
            echo ""
            echo -e "${RED}✗ x509-parser: FAILED${NC}"
        fi
        
        echo ""
        echo "───────────────────────────────────────────────────────"
        echo ""
    else
        echo -e "${YELLOW}[2/2] Skipping x509-parser benchmark (--skip-x509)${NC}"
        echo ""
    fi
fi

# Calculate elapsed time
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))
MINUTES=$((ELAPSED / 60))
SECONDS=$((ELAPSED % 60))

# Print final summary
echo ""
echo "╔═══════════════════════════════════════════════════════╗"
echo "║              FINAL SUMMARY                            ║"
echo "╚═══════════════════════════════════════════════════════╝"
echo ""

if [[ -z "$ONLY_SUITE" ]] || [[ "$ONLY_SUITE" == "frama-c" ]]; then
    if [[ $FRAMA_C_RESULT -eq 0 ]]; then
        echo -e "frama-c-problems: ${GREEN}✓ PASSED${NC}"
    else
        echo -e "frama-c-problems: ${RED}✗ FAILED${NC}"
    fi
fi

if [[ -z "$ONLY_SUITE" ]] || [[ "$ONLY_SUITE" == "x509" ]]; then
    if [[ $SKIP_X509 -eq 0 ]]; then
        if [[ $X509_RESULT -eq 0 ]]; then
            echo -e "x509-parser:      ${GREEN}✓ PASSED${NC}"
        else
            echo -e "x509-parser:      ${RED}✗ FAILED${NC}"
        fi
    else
        echo -e "x509-parser:      ${YELLOW}⊝ SKIPPED${NC}"
    fi
fi

echo ""
echo "Total time: ${MINUTES}m ${SECONDS}s"
echo ""

# Determine exit code
if [[ $FRAMA_C_RESULT -ne 0 ]] || [[ $X509_RESULT -ne 0 ]]; then
    echo -e "${RED}Some benchmarks failed!${NC}"
    exit 1
else
    echo -e "${GREEN}All benchmarks passed!${NC}"
    exit 0
fi

