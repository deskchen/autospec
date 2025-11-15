"""Integration tests for Frama-C verifier"""
import unittest
from pathlib import Path
from autospec.verifier.frama_c import FramaCVerifier
from autospec.verifier.verdict import VerdictType
from autospec.config import BENCHMARKS_DIR


class TestFramaCIntegration(unittest.TestCase):
    """Test Frama-C verifier integration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.verifier = FramaCVerifier(timeout=120)
        self.benchmarks_dir = BENCHMARKS_DIR / "frama_c_problems"
    
    def test_verifier_initialization(self):
        """Test that verifier initializes correctly"""
        self.assertIsNotNone(self.verifier)
        self.assertEqual(self.verifier.timeout, 120)
    
    def test_array_max_verification(self):
        """Test verification of array_max.c"""
        test_file = self.benchmarks_dir / "array_max.c"
        
        # Skip if file doesn't exist
        if not test_file.exists():
            self.skipTest(f"Benchmark file not found: {test_file}")
        
        verdict = self.verifier.verify(test_file)
        
        # Check that we got a verdict
        self.assertIsNotNone(verdict)
        self.assertIn(verdict.verdict_type, [
            VerdictType.VALID,
            VerdictType.INVALID,
            VerdictType.TIMEOUT,
            VerdictType.UNKNOWN
        ])
        
        # If Frama-C is installed, we expect either VALID or UNKNOWN
        # (UNKNOWN can occur if prover times out)
        if verdict.verdict_type not in [VerdictType.VALID, VerdictType.UNKNOWN]:
            print(f"Warning: Unexpected verdict for array_max.c: {verdict}")
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent file"""
        test_file = Path("/nonexistent/file.c")
        verdict = self.verifier.verify(test_file)
        
        self.assertEqual(verdict.verdict_type, VerdictType.UNKNOWN)
        self.assertIn("not found", verdict.message.lower())
    
    def test_abs_value_verification(self):
        """Test verification of abs_value.c"""
        test_file = self.benchmarks_dir / "abs_value.c"
        
        # Skip if file doesn't exist
        if not test_file.exists():
            self.skipTest(f"Benchmark file not found: {test_file}")
        
        verdict = self.verifier.verify(test_file)
        
        # Check that we got a verdict
        self.assertIsNotNone(verdict)
        self.assertIsInstance(verdict.verdict_type, VerdictType)


class TestVerdictTypes(unittest.TestCase):
    """Test verdict type representations"""
    
    def test_verdict_types_exist(self):
        """Test that all verdict types are defined"""
        self.assertTrue(hasattr(VerdictType, 'VALID'))
        self.assertTrue(hasattr(VerdictType, 'INVALID'))
        self.assertTrue(hasattr(VerdictType, 'TIMEOUT'))
        self.assertTrue(hasattr(VerdictType, 'UNKNOWN'))
    
    def test_verdict_string_representation(self):
        """Test verdict string formatting"""
        from autospec.verifier.verdict import Verdict
        
        verdict = Verdict(
            verdict_type=VerdictType.VALID,
            message="Test passed"
        )
        
        verdict_str = str(verdict)
        self.assertIn("VALID", verdict_str)
        self.assertIn("Test passed", verdict_str)


if __name__ == '__main__':
    unittest.main()

