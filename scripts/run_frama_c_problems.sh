#!/bin/bash
# Script to run AutoSpec verification on frama-c-problems benchmarks

# Don't exit on error - we handle verification failures ourselves
set +e

# Ensure OPAM environment is loaded (for Docker container)
if command -v opam &> /dev/null; then
    eval $(opam env) 2>/dev/null || true
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
# Default benchmarks directory (can be overridden with -d/--dir)
DEFAULT_BENCHMARKS_DIR="$PROJECT_ROOT/benchmarks/frama-c-problems/ground-truth"

# Color codes for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TOTAL=0
PASSED=0
FAILED=0
TIMEOUT=0
UNKNOWN=0

# Available categories
CATEGORIES=(
    "arrays_and_loops"
    "general_wp_problems"
    "immutable_arrays"
    "loops"
    "miscellaneous"
    "more_arrays"
    "mutable_arrays"
    "pointers"
)

usage() {
    echo "Usage: $0 [CATEGORY] [OPTIONS]"
    echo ""
    echo "Run AutoSpec verification on frama-c-problems benchmarks"
    echo ""
    echo "Arguments:"
    echo "  CATEGORY        Category to test (optional, tests all if not specified)"
    echo ""
    echo "Available categories:"
    for cat in "${CATEGORIES[@]}"; do
        echo "  - $cat"
    done
    echo ""
    echo "Options:"
    echo "  -d, --dir DIR   Benchmarks directory (default: benchmarks/frama-c-problems/ground-truth)"
    echo "  -v, --verbose   Show detailed Frama-C output"
    echo "  -h, --help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                          # Test all categories (default directory)"
    echo "  $0 loops                    # Test only loops category"
    echo "  $0 arrays_and_loops -v      # Test arrays_and_loops with verbose output"
    echo "  $0 -d outputs/annotated     # Test files in outputs/annotated directory"
    echo "  $0 loops -d outputs/annotated -v  # Test loops category in outputs/annotated with verbose"
}

# Parse arguments
CATEGORY=""
VERBOSE=""
BENCHMARKS_DIR="$DEFAULT_BENCHMARKS_DIR"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            usage
            exit 0
            ;;
        -d|--dir)
            BENCHMARKS_DIR="$2"
            shift 2
            ;;
        -v|--verbose)
            VERBOSE="--verbose"
            shift
            ;;
        *)
            CATEGORY="$1"
            shift
            ;;
    esac
done

# Resolve relative paths to absolute
if [[ ! "$BENCHMARKS_DIR" =~ ^/ ]]; then
    BENCHMARKS_DIR="$PROJECT_ROOT/$BENCHMARKS_DIR"
fi

# Function to verify a single file
verify_file() {
    local file="$1"
    local relative_path="${file#$PROJECT_ROOT/}"
    
    echo -n "Testing $relative_path ... "
    
    # Run verification
    output=$(python3 -m autospec.cli.main verify "$file" $VERBOSE 2>&1)
    exit_code=$?
    
    # Parse result
    # Check INVALID first since "VALID:" is a substring of "INVALID:"
    if echo "$output" | grep -q "INVALID:"; then
        echo -e "${RED}INVALID${NC}"
        ((FAILED++))
    elif echo "$output" | grep -q "TIMEOUT:"; then
        echo -e "${YELLOW}TIMEOUT${NC}"
        ((TIMEOUT++))
    elif echo "$output" | grep -q "VALID:"; then
        echo -e "${GREEN}VALID${NC}"
        ((PASSED++))
    else
        echo -e "${YELLOW}UNKNOWN${NC}"
        ((UNKNOWN++))
    fi
    
    ((TOTAL++))
    
    # Show detailed output if verbose
    if [[ -n "$VERBOSE" ]]; then
        echo "$output"
        echo ""
    fi
}

# Function to test a category
test_category() {
    local cat="$1"
    local cat_dir="$BENCHMARKS_DIR/$cat"
    
    if [[ ! -d "$cat_dir" ]]; then
        echo "Category not found: $cat"
        return 1
    fi
    
    echo ""
    echo "=========================================="
    echo "Testing category: $cat"
    echo "=========================================="
    
    # Find all .c files in the category
    while IFS= read -r -d '' file; do
        verify_file "$file"
    done < <(find "$cat_dir" -name "*.c" -type f -print0 | sort -z)
}

# Main execution
echo "=== AutoSpec Frama-C Problems Benchmark Runner ==="
echo "Benchmarks directory: $BENCHMARKS_DIR"

cd "$PROJECT_ROOT"

if [[ -n "$CATEGORY" ]]; then
    # Test specific category
    test_category "$CATEGORY"
else
    # Test all categories
    for cat in "${CATEGORIES[@]}"; do
        if [[ -d "$BENCHMARKS_DIR/$cat" ]]; then
            test_category "$cat"
        fi
    done
fi

# Print summary
echo ""
echo "=========================================="
echo "SUMMARY"
echo "=========================================="
echo "Total tests:    $TOTAL"
echo -e "${GREEN}Passed (VALID): $PASSED${NC}"
echo -e "${RED}Failed (INVALID): $FAILED${NC}"
echo -e "${YELLOW}Timeout:        $TIMEOUT${NC}"
echo -e "${YELLOW}Unknown:        $UNKNOWN${NC}"
echo "=========================================="

# Calculate success rate
if [[ $TOTAL -gt 0 ]]; then
    SUCCESS_RATE=$((PASSED * 100 / TOTAL))
    echo "Success rate: $SUCCESS_RATE%"
fi

# Exit with appropriate code
if [[ $FAILED -gt 0 ]]; then
    exit 1
else
    exit 0
fi

