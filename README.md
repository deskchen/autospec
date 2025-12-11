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

# Run a specific category
./scripts/run_frama_c_problems.sh loops
./scripts/run_frama_c_problems.sh arrays_and_loops -v
```

## Automated Spec Generation with vLLM

```bash
# (Terminal 1 inside docker)
python3 -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen3-32B \
  --port 8000 --dtype auto --gpu-memory-utilization 0.80
```

```bash
# (Terminal 2 inside docker)
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


