"""Union-Find / Disjoint Set Union with path compression and union by rank."""


def union_find_demo(edges: list[tuple], node_count: int) -> list[dict]:
    steps = []
    parent = list(range(node_count))
    rank = [0] * node_count

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

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

    steps.append({"step": len(steps) + 1, "current": 0,
                  "description": f"Initialize DSU with {node_count} elements"})

    merged = set()
    for u, v, w in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            steps.append({"step": len(steps) + 1, "current": u,
                          "edge_active": [u, v], "visited": list(merged),
                          "description": f"Union({u},{v}): already in same set (root={ru})"})
        else:
            union(u, v)
            merged.add(u)
            merged.add(v)
            steps.append({"step": len(steps) + 1, "current": u,
                          "edge_active": [u, v], "visited": list(merged),
                          "highlighted": [u, v],
                          "description": f"Union({u},{v}): merge sets {ru} and {rv}"})

    # Show final sets
    sets = {}
    for i in range(node_count):
        r = find(i)
        sets.setdefault(r, []).append(i)

    steps.append({"step": len(steps) + 1,
                  "description": f"Final sets: {list(sets.values())}"})
    return steps


"""Kahn's Algorithm — Topological Sort using BFS and in-degree."""
from collections import deque


def kahns_algorithm(adj: dict, node_count: int) -> list[dict]:
    steps = []
    in_degree = {n: 0 for n in range(node_count)}
    for u in adj:
        for v, _ in adj.get(u, []):
            in_degree[v] = in_degree.get(v, 0) + 1

    queue = deque([n for n in range(node_count) if in_degree.get(n, 0) == 0])
    order = []

    steps.append({"step": len(steps) + 1,
                  "frontier": list(queue),
                  "description": f"Initial zero in-degree nodes: {list(queue)}"})

    while queue:
        node = queue.popleft()
        order.append(node)
        steps.append({"step": len(steps) + 1, "current": node, "visited": list(order),
                      "frontier": list(queue),
                      "description": f"Process {node} (in-degree was 0)"})

        for neighbor, _ in adj.get(node, []):
            in_degree[neighbor] -= 1
            steps.append({"step": len(steps) + 1, "current": node,
                          "edge_active": [node, neighbor], "visited": list(order),
                          "description": f"Decrement in-degree of {neighbor} → {in_degree[neighbor]}"})
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) == node_count:
        steps.append({"step": len(steps) + 1, "path": order,
                      "description": f"Topological order: {order}"})
    else:
        steps.append({"step": len(steps) + 1,
                      "description": "Cycle detected — no valid topological order"})
    return steps


"""Cycle Detection in Directed Graph using DFS coloring."""


def cycle_detection_directed(adj: dict, node_count: int) -> list[dict]:
    steps = []
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {i: WHITE for i in range(node_count)}
    cycle_edges = []

    def dfs(u):
        color[u] = GRAY
        steps.append({"step": len(steps) + 1, "current": u,
                      "visited": [n for n in range(node_count) if color[n] == BLACK],
                      "frontier": [n for n in range(node_count) if color[n] == GRAY],
                      "description": f"Visit {u} (mark GRAY)"})

        for v, _ in adj.get(u, []):
            if color[v] == GRAY:
                cycle_edges.append([u, v])
                steps.append({"step": len(steps) + 1, "edge_active": [u, v],
                              "description": f"Back edge {u}→{v}: CYCLE DETECTED!"})
                return True
            if color[v] == WHITE:
                steps.append({"step": len(steps) + 1, "edge_active": [u, v],
                              "description": f"Explore {u}→{v}"})
                if dfs(v):
                    return True
        color[u] = BLACK
        return False

    has_cycle = False
    for i in range(node_count):
        if color[i] == WHITE:
            if dfs(i):
                has_cycle = True
                break

    steps.append({"step": len(steps) + 1,
                  "description": f"{'Cycle found!' if has_cycle else 'No cycle — graph is a DAG'}"})
    return steps


"""Cycle Detection in Undirected Graph using DFS."""


def cycle_detection_undirected(adj: dict, node_count: int) -> list[dict]:
    steps = []
    visited = set()

    def dfs(u, parent):
        visited.add(u)
        steps.append({"step": len(steps) + 1, "current": u,
                      "visited": list(visited),
                      "description": f"Visit {u} (parent={parent})"})

        for v, _ in adj.get(u, []):
            if v not in visited:
                steps.append({"step": len(steps) + 1, "edge_active": [u, v],
                              "description": f"Explore {u}→{v}"})
                if dfs(v, u):
                    return True
            elif v != parent:
                steps.append({"step": len(steps) + 1, "edge_active": [u, v],
                              "description": f"Back edge {u}→{v}: CYCLE DETECTED!"})
                return True
        return False

    has_cycle = False
    for i in range(node_count):
        if i not in visited:
            if dfs(i, -1):
                has_cycle = True
                break

    steps.append({"step": len(steps) + 1,
                  "description": f"{'Cycle found!' if has_cycle else 'No cycle — graph is acyclic'}"})
    return steps


"""Johnson's Algorithm — All-pairs shortest paths for sparse graphs — O(V²·log V + V·E)."""
import heapq


def johnsons_algorithm(adj: dict, node_count: int) -> list[dict]:
    steps = []
    INF = 999999

    # Step 1: Add virtual node connected to all nodes with weight 0
    virtual = node_count
    new_adj = {i: list(adj.get(i, [])) for i in range(node_count)}
    new_adj[virtual] = [(i, 0) for i in range(node_count)]

    # Step 2: Run Bellman-Ford from virtual node
    dist_h = {i: INF for i in range(node_count + 1)}
    dist_h[virtual] = 0

    steps.append({"step": len(steps) + 1,
                  "description": "Step 1: Run Bellman-Ford from virtual node to get reweighting function h()"})

    for _ in range(node_count):
        for u in new_adj:
            for v, w in new_adj[u]:
                if dist_h[u] + w < dist_h[v]:
                    dist_h[v] = dist_h[u] + w

    # Check negative cycle
    for u in new_adj:
        for v, w in new_adj[u]:
            if dist_h[u] + w < dist_h[v]:
                steps.append({"step": len(steps) + 1,
                              "description": "Negative cycle detected!"})
                return steps

    steps.append({"step": len(steps) + 1,
                  "distances": {str(k): v for k, v in dist_h.items() if k != virtual},
                  "description": f"h values: {dict((k, dist_h[k]) for k in range(node_count))}"})

    # Step 3: Reweight edges and run Dijkstra from each vertex
    results = [[INF] * node_count for _ in range(node_count)]

    for source in range(node_count):
        dist = {i: INF for i in range(node_count)}
        dist[source] = 0
        pq = [(0, source)]
        visited = set()

        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            for v, w in adj.get(u, []):
                # Reweighted edge
                rw = w + dist_h[u] - dist_h[v]
                if d + rw < dist[v]:
                    dist[v] = d + rw
                    heapq.heappush(pq, (dist[v], v))

        for v in range(node_count):
            if dist[v] < INF:
                results[source][v] = dist[v] - dist_h[source] + dist_h[v]

        steps.append({"step": len(steps) + 1, "current": source,
                      "distances": {str(k): (v if v < INF else -1) for k, v in dist.items()},
                      "description": f"Dijkstra from {source}: shortest distances computed"})

    steps.append({"step": len(steps) + 1,
                  "table": [[v if v < INF else -1 for v in row] for row in results],
                  "description": "Johnson's algorithm complete — all-pairs shortest paths"})
    return steps
