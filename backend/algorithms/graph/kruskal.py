"""Kruskal's MST — O(E log E) time, O(V) space"""


def kruskal(edges: list[tuple], node_count: int) -> list[dict]:
    steps = []
    sorted_edges = sorted(edges, key=lambda e: e[2])
    parent = list(range(node_count))
    rank = [0] * node_count
    mst = []
    mst_nodes = set()

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    for u, v, w in sorted_edges:
        steps.append({
            "step": len(steps) + 1,
            "current": u,
            "edge_active": [u, v],
            "visited": list(mst_nodes),
            "mst_edges": [list(e[:2]) for e in mst],
            "description": f"Consider edge {u}–{v} (weight {w})",
        })

        if union(u, v):
            mst.append((u, v, w))
            mst_nodes.add(u)
            mst_nodes.add(v)
            steps.append({
                "step": len(steps) + 1,
                "current": v,
                "edge_active": [u, v],
                "visited": list(mst_nodes),
                "mst_edges": [list(e[:2]) for e in mst],
                "description": f"Add edge {u}–{v} to MST (weight {w})",
            })
        else:
            steps.append({
                "step": len(steps) + 1,
                "current": u,
                "visited": list(mst_nodes),
                "mst_edges": [list(e[:2]) for e in mst],
                "description": f"Skip {u}–{v} (would form cycle)",
            })

        if len(mst) == node_count - 1:
            break

    total = sum(e[2] for e in mst)
    steps.append({
        "step": len(steps) + 1,
        "visited": list(mst_nodes),
        "mst_edges": [list(e[:2]) for e in mst],
        "description": f"MST complete! Total weight = {total}",
    })
    return steps
