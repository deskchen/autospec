"""LLM client interface (placeholder for future implementation)"""
from typing import Optional


class LLMClient:
    """Client for interacting with LLMs (placeholder)"""
    
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        
    def generate_specification(self, code: str, prompt: str) -> str:
        """Generate ACSL specification from code (placeholder)"""
        # TODO: Implement LLM integration
        # This will be used with local models later
        raise NotImplementedError("LLM integration not yet implemented")

