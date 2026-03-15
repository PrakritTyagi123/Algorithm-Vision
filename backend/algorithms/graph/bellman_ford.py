"""Bellman-Ford — O(V·E) time, O(V) space. Handles negative weights."""


def bellman_ford(adj: dict, edges: list[tuple], node_count: int, start: int) -> list[dict]:
    steps = []
    dist = {i: float('inf') for i in range(node_count)}
    dist[start] = 0
    parent = {start: None}

    def _safe_dist():
        return {str(k): (v if v != float('inf') else 999999) for k, v in dist.items()}

    for iteration in range(node_count - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float('inf') and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                updated = True
                steps.append({
                    "step": len(steps)+1, "current": v,
                    "edge_active": [u, v],
                    "visited": [n for n in range(node_count) if dist[n] != float('inf')],
                    "distances": _safe_dist(),
                    "description": f"Iter {iteration+1}: relax {u}→{v}, dist[{v}]={dist[v]}",
                })
        if not updated:
            steps.append({"step": len(steps)+1,
                          "distances": _safe_dist(),
                          "description": f"No updates in iteration {iteration+1}, done early"})
            break

    # Check for negative cycles
    for u, v, w in edges:
        if dist[u] != float('inf') and dist[u] + w < dist[v]:
            steps.append({"step": len(steps)+1,
                          "description": "Negative weight cycle detected!"})
            return steps

    steps.append({
        "step": len(steps)+1,
        "visited": list(range(node_count)),
        "distances": _safe_dist(),
        "description": "Bellman-Ford complete",
    })
    return steps
