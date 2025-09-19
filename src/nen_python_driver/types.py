"""
Type definitions for the NenDB Python driver
"""

from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass, field
from enum import Enum


class AlgorithmStatus(Enum):
    """Status of algorithm execution"""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class GraphNode:
    """Represents a node in the graph"""

    id: int
    labels: List[str]
    properties: Dict[str, Any]

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError("Node ID must be an integer")
        if not isinstance(self.labels, list):
            raise ValueError("Labels must be a list")
        if not isinstance(self.properties, dict):
            raise ValueError("Properties must be a dictionary")


@dataclass
class GraphEdge:
    """Represents an edge in the graph"""

    id: int
    source: int
    target: int
    type: str
    properties: Dict[str, Any]

    def __post_init__(self):
        if not isinstance(self.id, int):
            raise ValueError("Edge ID must be an integer")
        if not isinstance(self.source, int):
            raise ValueError("Source node ID must be an integer")
        if not isinstance(self.target, int):
            raise ValueError("Target node ID must be an integer")
        if not isinstance(self.type, str):
            raise ValueError("Edge type must be a string")
        if not isinstance(self.properties, dict):
            raise ValueError("Properties must be a dictionary")


@dataclass
class AlgorithmResult:
    """Base class for algorithm results"""

    algorithm: str
    status: AlgorithmStatus
    message: str
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if not isinstance(self.algorithm, str):
            raise ValueError("Algorithm name must be a string")
        if not isinstance(self.status, AlgorithmStatus):
            raise ValueError("Status must be an AlgorithmStatus enum value")
        if not isinstance(self.message, str):
            raise ValueError("Message must be a string")


@dataclass
class BFSResult(AlgorithmResult):
    """Result of BFS algorithm execution"""

    visited_nodes: List[int] = field(default_factory=list)
    path: List[int] = field(default_factory=list)
    depth: int = 0

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.visited_nodes, list):
            raise ValueError("Visited nodes must be a list")
        if not isinstance(self.path, list):
            raise ValueError("Path must be a list")
        if not isinstance(self.depth, int):
            raise ValueError("Depth must be an integer")


@dataclass
class DijkstraResult(AlgorithmResult):
    """Result of Dijkstra algorithm execution"""

    shortest_path: List[int] = field(default_factory=list)
    total_cost: float = 0.0
    path_details: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.shortest_path, list):
            raise ValueError("Shortest path must be a list")
        if not isinstance(self.total_cost, (int, float)):
            raise ValueError("Total cost must be a number")
        if not isinstance(self.path_details, list):
            raise ValueError("Path details must be a list")


@dataclass
class PageRankResult(AlgorithmResult):
    """Result of PageRank algorithm execution"""

    node_scores: Dict[int, float] = field(default_factory=dict)
    iterations: int = 0
    convergence: bool = False

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.node_scores, dict):
            raise ValueError("Node scores must be a dictionary")
        if not isinstance(self.iterations, int):
            raise ValueError("Iterations must be an integer")
        if not isinstance(self.convergence, bool):
            raise ValueError("Convergence must be a boolean")


# Type aliases for convenience
NodeID = int
EdgeID = int
PropertyValue = Union[str, int, float, bool, None]
PropertyMap = Dict[str, PropertyValue]
