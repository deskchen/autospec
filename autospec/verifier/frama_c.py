"""Frama-C WP verification wrapper"""
import subprocess
import re
from pathlib import Path
from typing import Optional, List
from .verdict import Verdict, VerdictType
from ..config import FRAMA_C_COMMAND, FRAMA_C_TIMEOUT, FRAMA_C_WP_TIMEOUT


class FramaCVerifier:
    """Wrapper for Frama-C WP verification"""
    
    def __init__(self, timeout: int = FRAMA_C_TIMEOUT):
        self.timeout = timeout
        self.frama_c_cmd = FRAMA_C_COMMAND
        
    def verify(self, c_file: Path) -> Verdict:
        """Run Frama-C WP on a C file and return verdict"""
        if not c_file.exists():
            return Verdict(
                verdict_type=VerdictType.UNKNOWN,
                message=f"File not found: {c_file}"
            )
        
        try:
            # Run Frama-C with WP plugin
            # Note: We don't require termination proofs since benchmarks may not include loop variants
            cmd = [
                self.frama_c_cmd,
                "-generated-spec-custom", "terminates:skip",
                "-wp",
                f"-wp-timeout={FRAMA_C_WP_TIMEOUT}",
                "-wp-prover=alt-ergo",
                # "-warn-unsigned-overflow",  # Warn about potential overflows
                str(c_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            return self._parse_output(result.stdout, result.stderr, result.returncode)
            
        except subprocess.TimeoutExpired:
            return Verdict(
                verdict_type=VerdictType.TIMEOUT,
                message=f"Verification timed out after {self.timeout}s"
            )
        except FileNotFoundError:
            return Verdict(
                verdict_type=VerdictType.UNKNOWN,
                message=f"Frama-C not found. Please install Frama-C and ensure '{self.frama_c_cmd}' is in PATH"
            )
        except Exception as e:
            return Verdict(
                verdict_type=VerdictType.UNKNOWN,
                message=f"Verification error: {str(e)}"
            )
    
    def _parse_output(self, stdout: str, stderr: str, returncode: int) -> Verdict:
        """Parse Frama-C output to determine verdict"""
        output = stdout + stderr
        
        # Check for "Proved goals: X / X" pattern (all goals proven)
        proved_match = re.search(r'\[wp\] Proved goals:\s+(\d+)\s*/\s*(\d+)', output)
        if proved_match:
            proved = int(proved_match.group(1))
            total = int(proved_match.group(2))
            
            if proved == total and total > 0:
                return Verdict(
                    verdict_type=VerdictType.VALID,
                    message=f"All proof obligations verified ({proved}/{total} goals proven)",
                    details=output
                )
            elif proved < total:
                # Check if the failure is due to timeout
                timeout_count = len(re.findall(r'\[Timeout\]', output))
                if timeout_count > 0:
                    return Verdict(
                        verdict_type=VerdictType.TIMEOUT,
                        message=f"Verification incomplete: {timeout_count} goal(s) timed out ({proved}/{total} goals proven)",
                        details=output
                    )
                else:
                    return Verdict(
                        verdict_type=VerdictType.INVALID,
                        message=f"Some proof obligations failed ({proved}/{total} goals proven)",
                        details=output
                    )
        
        # Look for "Valid" in output (older Frama-C versions or different output format)
        if "Valid" in output and returncode == 0:
            valid_count = len(re.findall(r"Valid", output))
            return Verdict(
                verdict_type=VerdictType.VALID,
                message=f"All proof obligations verified ({valid_count} valid)",
                details=output
            )
        
        # Check for timeouts or unknown results
        if "Timeout" in output or "timeout" in output.lower():
            return Verdict(
                verdict_type=VerdictType.TIMEOUT,
                message="Verification timed out",
                details=output
            )
        
        if "Unknown" in output:
            return Verdict(
                verdict_type=VerdictType.UNKNOWN,
                message="Some proof obligations could not be verified",
                details=output
            )
        
        # Check for invalid results
        if "Invalid" in output or (returncode != 0 and "error" in output.lower()):
            return Verdict(
                verdict_type=VerdictType.INVALID,
                message="Verification failed",
                details=output
            )
        
        # Default case
        return Verdict(
            verdict_type=VerdictType.UNKNOWN,
            message="Could not determine verification result",
            details=output
        )

