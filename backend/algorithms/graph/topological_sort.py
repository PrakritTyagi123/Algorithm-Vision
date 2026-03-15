"""Topological Sort (Kahn's BFS) — O(V+E) time, O(V) space"""
from collections import deque


def topological_sort(adj: dict, node_count: int) -> list[dict]:
    steps = []
    in_degree = {n: 0 for n in adj}
    for u in adj:
        for v, _ in adj[u]:
            in_degree[v] = in_degree.get(v, 0) + 1

    queue = deque([n for n in adj if in_degree[n] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        steps.append({
            "step": len(steps)+1, "current": node,
            "visited": list(order), "frontier": list(queue),
            "description": f"Process node {node} (in-degree=0)",
        })

        for neighbor, _ in adj.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
                steps.append({
                    "step": len(steps)+1, "current": node,
                    "visited": list(order), "frontier": list(queue),
                    "edge_active": [node, neighbor],
                    "description": f"Decrement {neighbor}, now in-degree=0",
                })

    if len(order) == node_count:
        steps.append({"step": len(steps)+1, "path": order,
                      "description": f"Topological order: {order}"})
    else:
        steps.append({"step": len(steps)+1,
                      "description": "Cycle detected — no valid topological order!"})
    return steps
