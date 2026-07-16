OPENIE_PROMPT = """
Extract knowledge triples from the passage.

Return ONLY valid JSON.

Format:

[
    {
        "subject": "...",
        "predicate": "...",
        "object": "..."
    }
]

Passage:

{text}
"""