"""
NenDB Python Driver
A high-performance Python client for the NenDB graph database
"""

from .client import NenDBClient
from .exceptions import NenDBError
from .types import GraphNode, GraphEdge, AlgorithmResult

__version__ = "0.1.0"
__author__ = "Nen Team"
__email__ = "team@nen.co"

__all__ = [
    "NenDBClient",
    "NenDBError",
    "GraphNode",
    "GraphEdge",
    "AlgorithmResult",
]
