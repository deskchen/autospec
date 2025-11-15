"""Verification verdict representations"""
from enum import Enum
from dataclasses import dataclass
from typing import Optional


class VerdictType(Enum):
    """Possible verification outcomes"""
    VALID = "valid"
    INVALID = "invalid"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"


@dataclass
class Verdict:
    """Represents a verification result"""
    verdict_type: VerdictType
    message: str
    details: Optional[str] = None
    
    def is_valid(self) -> bool:
        """Check if verification was successful"""
        return self.verdict_type == VerdictType.VALID
    
    def __str__(self) -> str:
        """String representation of verdict"""
        return f"{self.verdict_type.value.upper()}: {self.message}"

