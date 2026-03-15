"""Dijkstra's Shortest Path — O(V² or E log V) time, O(V) space"""
import heapq


def dijkstra(adj: dict, start: int, end: int = None) -> list[dict]:
    steps = []
    dist = {node: float('inf') for node in adj}
    dist[start] = 0
    visited = set()
    parent = {start: None}
    pq = [(0, start)]

    def _safe_dist():
        return {str(k): (v if v != float('inf') else 999999) for k, v in dist.items()}

    while pq:
        d, u = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)

        steps.append({
            "step": len(steps)+1, "current": u,
            "visited": list(visited),
            "distances": _safe_dist(),
            "description": f"Process node {u} (dist={d})",
        })

        if end is not None and u == end:
            path = _reconstruct(parent, start, end)
            steps.append({"step": len(steps)+1, "visited": list(visited),
                          "path": path,
                          "distances": _safe_dist(),
                          "description": f"Shortest path to {end}: cost={d}"})
            return steps

        for v, w in adj.get(u, []):
            if v not in visited and d + w < dist[v]:
                dist[v] = d + w
                parent[v] = u
                heapq.heappush(pq, (dist[v], v))
                steps.append({
                    "step": len(steps)+1, "current": u,
                    "visited": list(visited),
                    "edge_active": [u, v],
                    "distances": _safe_dist(),
                    "description": f"Relax {u}→{v}: dist={dist[v]}",
                })

    if end is not None:
        steps.append({"step": len(steps)+1, "visited": list(visited),
                      "description": f"No path to {end}"})
    return steps


def _reconstruct(parent, start, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    return list(reversed(path))
