"""Configuration settings for AutoSpec"""
import os
from pathlib import Path

# Frama-C settings
FRAMA_C_COMMAND = os.getenv("FRAMA_C_COMMAND", "frama-c")
FRAMA_C_TIMEOUT = int(os.getenv("FRAMA_C_TIMEOUT", "10"))  # seconds
FRAMA_C_WP_TIMEOUT = int(os.getenv("FRAMA_C_WP_TIMEOUT", "10"))  # seconds per proof

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks"
FRAMA_C_PROBLEMS_DIR = BENCHMARKS_DIR / "frama_c_problems"

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
VERBOSE = os.getenv("VERBOSE", "false").lower() == "true"

