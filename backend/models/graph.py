"""
AlgoVision — Graph Model
Shared graph data structures used across graph algorithms.
"""

from __future__ import annotations
from typing import Optional


class GraphModel:
    """Simple adjacency-list graph representation."""

    def __init__(self, nodes: list[dict], edges: list[dict], directed: bool = False):
        self.nodes = nodes
        self.edges = edges
        self.directed = directed
        self.node_count = len(nodes)

        # Build adjacency list: {node_id: [(neighbor, weight), ...]}
        self.adj: dict[int, list[tuple[int, float]]] = {n["id"]: [] for n in nodes}
        for e in edges:
            self.adj[e["from"]].append((e["to"], e.get("weight", 1)))
            if not directed:
                self.adj[e["to"]].append((e["from"], e.get("weight", 1)))

    def get_unique_edges(self) -> list[tuple[int, int, float]]:
        """Return deduplicated edge list as (from, to, weight)."""
        seen = set()
        result = []
        for e in self.edges:
            key = (min(e["from"], e["to"]), max(e["from"], e["to"])) if not self.directed else (e["from"], e["to"])
            if key not in seen:
                seen.add(key)
                result.append((e["from"], e["to"], e.get("weight", 1)))
        return result
