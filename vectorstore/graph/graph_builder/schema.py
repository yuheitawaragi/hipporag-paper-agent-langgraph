from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass
class GraphNode:
    """
    Knowledge Graph node
    """

    id: str

    # 表示名
    name: str

    # entity type
    # 例:
    # Person
    # Organization
    # Concept
    entity_type: str = "Entity"


    metadata: Dict[str, Any] = field(
            default_factory=dict
        )



@dataclass
class GraphEdge:
    """
    Knowledge Graph edge
    """

    source: str

    target: str

    relation: str


    metadata: Dict[str, Any] = field(
            default_factory=dict
        )