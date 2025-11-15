"""Prompt templates for LLM specification generation"""

# Prompt templates for different specification types
PRECONDITION_PROMPT = """
Given the following C function, generate ACSL preconditions (requires clauses):

{code}

Generate preconditions that specify:
1. Valid pointer requirements
2. Array bounds requirements
3. Value constraints on parameters
"""

POSTCONDITION_PROMPT = """
Given the following C function, generate ACSL postconditions (ensures clauses):

{code}

Generate postconditions that specify:
1. Return value constraints
2. Modified memory state
3. Relationship between input and output
"""

LOOP_INVARIANT_PROMPT = """
Given the following C loop, generate ACSL loop invariants:

{code}

Generate loop invariants that:
1. Hold before and after each iteration
2. Help prove loop termination
3. Establish relationships between loop variables
"""

