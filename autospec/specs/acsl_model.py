"""In-memory representation of ACSL specifications"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class ACSLPrecondition:
    """Represents an ACSL precondition (requires clause)"""
    condition: str
    
    def to_acsl(self) -> str:
        """Convert to ACSL annotation string"""
        return f"//@ requires {self.condition};"


@dataclass
class ACSLPostcondition:
    """Represents an ACSL postcondition (ensures clause)"""
    condition: str
    
    def to_acsl(self) -> str:
        """Convert to ACSL annotation string"""
        return f"//@ ensures {self.condition};"


@dataclass
class ACSLLoopInvariant:
    """Represents an ACSL loop invariant"""
    invariant: str
    
    def to_acsl(self) -> str:
        """Convert to ACSL annotation string"""
        return f"//@ loop invariant {self.invariant};"


@dataclass
class ACSLFunctionSpec:
    """Complete ACSL specification for a function"""
    function_name: str
    preconditions: List[ACSLPrecondition]
    postconditions: List[ACSLPostcondition]
    loop_invariants: List[ACSLLoopInvariant]
    
    def to_acsl(self) -> str:
        """Convert to complete ACSL annotation block"""
        lines = []
        lines.append(f"/*@")
        for pre in self.preconditions:
            lines.append(f"  @ requires {pre.condition};")
        for post in self.postconditions:
            lines.append(f"  @ ensures {post.condition};")
        lines.append(f"  @*/")
        return "\n".join(lines)

