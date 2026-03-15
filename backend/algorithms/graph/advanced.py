"""Kosaraju's SCC — O(V+E) time"""
from collections import defaultdict


def kosaraju(adj: dict, node_count: int) -> list[dict]:
    steps = []
    visited = set()
    order = []

    # Pass 1: DFS fill order — emit steps
    def dfs1(u):
        visited.add(u)
        steps.append({
            "step": len(steps) + 1,
            "current": u,
            "visited": list(visited),
            "description": f"Pass 1: visit {u}",
        })
        for v, _ in adj.get(u, []):
            if v not in visited:
                steps.append({
                    "step": len(steps) + 1,
                    "current": u,
                    "edge_active": [u, v],
                    "visited": list(visited),
                    "description": f"Pass 1: explore {u}→{v}",
                })
                dfs1(v)
        order.append(u)

    for i in range(node_count):
        if i not in visited:
            dfs1(i)

    steps.append({
        "step": len(steps) + 1,
        "visited": list(visited),
        "description": f"Pass 1 done. Finish order: {order}",
    })

    # Build reverse graph
    radj = defaultdict(list)
    for u in adj:
        for v, w in adj[u]:
            radj[v].append((u, w))

    # Pass 2: DFS on reverse in reverse-finish order — emit steps
    visited.clear()
    sccs = []

    def dfs2(u, comp):
        visited.add(u)
        comp.append(u)
        steps.append({
            "step": len(steps) + 1,
            "current": u,
            "visited": list(visited),
            "highlighted": list(comp),
            "description": f"Pass 2: visit {u} (SCC building)",
        })
        for v, _ in radj.get(u, []):
            if v not in visited:
                dfs2(v, comp)

    for u in reversed(order):
        if u not in visited:
            comp = []
            dfs2(u, comp)
            sccs.append(comp)
            steps.append({
                "step": len(steps) + 1,
                "visited": list(visited),
                "highlighted": comp,
                "description": f"SCC found: {comp}",
            })

    steps.append({"step": len(steps) + 1, "description": f"Found {len(sccs)} SCCs"})
    return steps


"""Tarjan's SCC — O(V+E) time"""


def tarjan(adj: dict, node_count: int) -> list[dict]:
    steps = []
    idx_counter = [0]
    stack = []
    lowlink = {}
    index = {}
    on_stack = set()
    sccs = []

    def strongconnect(v):
        index[v] = lowlink[v] = idx_counter[0]
        idx_counter[0] += 1
        stack.append(v)
        on_stack.add(v)

        steps.append({"step": len(steps)+1, "current": v,
                      "visited": list(index.keys()),
                      "description": f"Visit {v} (index={index[v]})"})

        for w, _ in adj.get(v, []):
            if w not in index:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], index[w])

        if lowlink[v] == index[v]:
            comp = []
            while True:
                w = stack.pop()
                on_stack.discard(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(comp)
            steps.append({"step": len(steps)+1, "highlighted": comp,
                          "description": f"SCC: {comp}"})

    for v in range(node_count):
        if v not in index:
            strongconnect(v)

    return steps


"""Bridges — O(V+E) time"""


def find_bridges(adj: dict, node_count: int) -> list[dict]:
    steps = []
    disc = {}
    low = {}
    timer = [0]
    bridges = []

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1

        for v, _ in adj.get(u, []):
            if v not in disc:
                steps.append({"step": len(steps)+1, "current": u,
                              "edge_active": [u, v], "visited": list(disc.keys()),
                              "description": f"Explore {u}→{v}"})
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > disc[u]:
                    bridges.append([u, v])
                    steps.append({"step": len(steps)+1,
                                  "edge_active": [u, v],
                                  "mst_edges": list(bridges),
                                  "description": f"Bridge found: {u}–{v}"})
            elif v != parent:
                low[u] = min(low[u], disc[v])

    for i in range(node_count):
        if i not in disc:
            dfs(i, -1)

    steps.append({"step": len(steps)+1, "mst_edges": list(bridges),
                  "description": f"Found {len(bridges)} bridge(s)"})
    return steps


"""Articulation Points — O(V+E) time"""


def find_articulation_points(adj: dict, node_count: int) -> list[dict]:
    steps = []
    disc = {}
    low = {}
    timer = [0]
    ap = set()

    def dfs(u, parent):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0

        for v, _ in adj.get(u, []):
            if v not in disc:
                children += 1
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if parent == -1 and children > 1:
                    ap.add(u)
                if parent != -1 and low[v] >= disc[u]:
                    ap.add(u)
                    steps.append({"step": len(steps)+1, "current": u,
                                  "highlighted": list(ap),
                                  "description": f"Articulation point: {u}"})
            elif v != parent:
                low[u] = min(low[u], disc[v])

    for i in range(node_count):
        if i not in disc:
            dfs(i, -1)

    steps.append({"step": len(steps)+1, "highlighted": list(ap),
                  "description": f"Found {len(ap)} articulation point(s)"})
    return steps
