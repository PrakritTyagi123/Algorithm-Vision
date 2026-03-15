"""Borůvka's MST — O(E log V) time, O(V) space"""


def boruvka(edges: list[tuple], node_count: int) -> list[dict]:
    steps = []
    parent = list(range(node_count))
    rank = [0] * node_count
    mst = []
    num_components = node_count
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

    iteration = 0
    while num_components > 1:
        iteration += 1
        cheapest = [None] * node_count

        for u, v, w in edges:
            cu, cv = find(u), find(v)
            if cu == cv:
                continue
            if cheapest[cu] is None or w < cheapest[cu][0]:
                cheapest[cu] = (w, u, v)
            if cheapest[cv] is None or w < cheapest[cv][0]:
                cheapest[cv] = (w, u, v)

        steps.append({
            "step": len(steps) + 1,
            "current": 0,
            "visited": list(mst_nodes),
            "mst_edges": [list(e[:2]) for e in mst],
            "description": f"Iteration {iteration}: find cheapest edge per component",
        })

        for comp in range(node_count):
            if cheapest[comp] is not None:
                w, u, v = cheapest[comp]
                if find(u) != find(v):
                    union(u, v)
                    mst.append((u, v, w))
                    mst_nodes.add(u)
                    mst_nodes.add(v)
                    num_components -= 1
                    steps.append({
                        "step": len(steps) + 1,
                        "current": u,
                        "edge_active": [u, v],
                        "visited": list(mst_nodes),
                        "mst_edges": [list(e[:2]) for e in mst],
                        "description": f"Add edge {u}–{v} (weight {w})",
                    })

    total = sum(e[2] for e in mst)
    steps.append({
        "step": len(steps) + 1,
        "visited": list(mst_nodes),
        "mst_edges": [list(e[:2]) for e in mst],
        "description": f"Borůvka MST complete! Total weight = {total}",
    })
    return steps
