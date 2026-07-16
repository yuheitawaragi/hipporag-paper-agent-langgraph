from dataclasses import dataclass


@dataclass
class Triple:
    subject: str
    predicate: str
    object: str