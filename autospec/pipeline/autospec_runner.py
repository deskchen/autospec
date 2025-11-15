"""Main AutoSpec pipeline runner"""
from pathlib import Path
from typing import Optional
from ..analysis.c_parser import CParser
from ..verifier.frama_c import FramaCVerifier
from ..verifier.verdict import Verdict


class AutoSpecRunner:
    """Main pipeline for AutoSpec workflow"""
    
    def __init__(self, timeout: int = 60):
        self.verifier = FramaCVerifier(timeout=timeout)
        
    def run(self, c_file: Path) -> Verdict:
        """Run AutoSpec pipeline on a C file"""
        # For now, just run verification
        # Future: add LLM-based spec generation and iterative refinement
        
        # Parse the C file
        parser = CParser(c_file)
        try:
            parser.parse()
        except FileNotFoundError as e:
            from ..verifier.verdict import VerdictType
            return Verdict(
                verdict_type=VerdictType.UNKNOWN,
                message=str(e)
            )
        
        # Run verification
        verdict = self.verifier.verify(c_file)
        
        return verdict

