from dataclasses import dataclass


@dataclass
class Entity:
    mention: str
    canonical: str