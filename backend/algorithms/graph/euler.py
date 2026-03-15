"""Euler Path / Circuit — Hierholzer's Algorithm — O(V+E) time"""
from collections import defaultdict


def euler_path(adj: dict, node_count: int) -> list[dict]:
    steps = []

    # Build mutable adjacency with edge counts
    graph = defaultdict(list)
    degree = defaultdict(int)
    for u in adj:
        for v, w in adj[u]:
            graph[u].append(v)
            degree[u] += 1

    # Find start node: odd-degree vertex or 0
    odd_vertices = [v for v in range(node_count) if degree[v] % 2 == 1]
    if len(odd_vertices) == 2:
        start = odd_vertices[0]
        steps.append({"step": len(steps) + 1,
                      "description": f"Euler PATH exists (odd-degree vertices: {odd_vertices})"})
    elif len(odd_vertices) == 0:
        start = next((v for v in range(node_count) if degree[v] > 0), 0)
        steps.append({"step": len(steps) + 1,
                      "description": "Euler CIRCUIT exists (all vertices have even degree)"})
    else:
        steps.append({"step": len(steps) + 1,
                      "description": f"No Euler path/circuit ({len(odd_vertices)} odd-degree vertices)"})
        return steps

    # Hierholzer's algorithm using edge tracking
    adj_copy = defaultdict(list)
    for u in graph:
        adj_copy[u] = list(graph[u])

    stack = [start]
    path = []
    visited_edges = []

    while stack:
        v = stack[-1]
        if adj_copy[v]:
            u = adj_copy[v].pop()
            # Remove reverse edge for undirected
            if u in adj_copy and v in adj_copy[u]:
                adj_copy[u].remove(v)
            stack.append(u)
            visited_edges.append([v, u])
            steps.append({
                "step": len(steps) + 1,
                "current": u,
                "edge_active": [v, u],
                "edges_visited": [list(e) for e in visited_edges],
                "description": f"Traverse {v} → {u}",
            })
        else:
            path.append(stack.pop())

    path.reverse()
    steps.append({
        "step": len(steps) + 1,
        "path": path,
        "description": f"Euler path: {' → '.join(map(str, path))}",
    })
    return steps
