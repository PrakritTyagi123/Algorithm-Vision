"""Prim's MST — O(V²) or O(E log V) time, O(V) space"""
import heapq


def prim(adj: dict, start: int = 0) -> list[dict]:
    steps = []
    visited = set()
    mst = []
    pq = [(0, start, -1)]  # (weight, node, parent)

    while pq:
        w, u, p = heapq.heappop(pq)
        if u in visited:
            continue
        visited.add(u)
        if p >= 0:
            mst.append([p, u])

        steps.append({
            "step": len(steps)+1, "current": u,
            "visited": list(visited),
            "mst_edges": list(mst),
            "description": f"Add node {u}" + (f" via edge {p}–{u} (w={w})" if p >= 0 else ""),
        })

        for v, weight in adj.get(u, []):
            if v not in visited:
                heapq.heappush(pq, (weight, v, u))
                steps.append({
                    "step": len(steps)+1, "current": u,
                    "visited": list(visited),
                    "edge_active": [u, v],
                    "mst_edges": list(mst),
                    "description": f"Consider edge {u}–{v} (w={weight})",
                })

    steps.append({
        "step": len(steps)+1,
        "visited": list(visited),
        "mst_edges": list(mst),
        "description": "Prim's MST complete!",
    })
    return steps
