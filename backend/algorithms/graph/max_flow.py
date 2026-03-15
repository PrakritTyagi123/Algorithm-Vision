"""Ford-Fulkerson / Edmonds-Karp Max Flow — O(V·E²) time"""
from collections import defaultdict, deque


def ford_fulkerson(adj: dict, node_count: int, source: int, sink: int) -> list[dict]:
    """Ford-Fulkerson using DFS for augmenting paths."""
    steps = []
    capacity = defaultdict(lambda: defaultdict(int))
    graph = defaultdict(set)

    for u in adj:
        for v, w in adj[u]:
            capacity[u][v] += w
            graph[u].add(v)
            graph[v].add(u)

    max_flow = 0

    def dfs_path(s, t, visited):
        if s == t:
            return [t]
        visited.add(s)
        for v in graph[s]:
            if v not in visited and capacity[s][v] > 0:
                path = dfs_path(v, t, visited)
                if path:
                    return [s] + path
        return None

    iteration = 0
    while True:
        path = dfs_path(source, sink, set())
        if not path:
            break
        iteration += 1

        # Find bottleneck
        bottleneck = min(capacity[path[i]][path[i + 1]] for i in range(len(path) - 1))

        steps.append({
            "step": len(steps) + 1,
            "path": path,
            "current": source,
            "description": f"Iteration {iteration}: augmenting path {' → '.join(map(str, path))}, flow={bottleneck}",
        })

        # Update capacities
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            capacity[u][v] -= bottleneck
            capacity[v][u] += bottleneck
            steps.append({
                "step": len(steps) + 1,
                "edge_active": [u, v],
                "description": f"Update capacity {u}→{v}: remaining={capacity[u][v]}",
            })

        max_flow += bottleneck

    steps.append({
        "step": len(steps) + 1,
        "description": f"Maximum flow = {max_flow}",
    })
    return steps


def edmonds_karp(adj: dict, node_count: int, source: int, sink: int) -> list[dict]:
    """Edmonds-Karp: Ford-Fulkerson with BFS for shortest augmenting path."""
    steps = []
    capacity = defaultdict(lambda: defaultdict(int))
    graph = defaultdict(set)

    for u in adj:
        for v, w in adj[u]:
            capacity[u][v] += w
            graph[u].add(v)
            graph[v].add(u)

    max_flow = 0
    iteration = 0

    while True:
        # BFS to find shortest augmenting path
        parent = {source: None}
        visited = {source}
        queue = deque([source])

        while queue:
            u = queue.popleft()
            if u == sink:
                break
            for v in graph[u]:
                if v not in visited and capacity[u][v] > 0:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)

        if sink not in parent:
            break

        iteration += 1

        # Reconstruct path
        path = []
        v = sink
        while v is not None:
            path.append(v)
            v = parent[v]
        path.reverse()

        bottleneck = min(capacity[path[i]][path[i + 1]] for i in range(len(path) - 1))

        steps.append({
            "step": len(steps) + 1,
            "current": source,
            "path": path,
            "visited": list(visited),
            "description": f"BFS iteration {iteration}: path {' → '.join(map(str, path))}, flow={bottleneck}",
        })

        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            capacity[u][v] -= bottleneck
            capacity[v][u] += bottleneck

        max_flow += bottleneck
        steps.append({
            "step": len(steps) + 1,
            "current": sink,
            "visited": list(visited),
            "description": f"Total flow so far: {max_flow}",
        })

    steps.append({
        "step": len(steps) + 1,
        "current": source,
        "description": f"Maximum flow = {max_flow}",
    })
    return steps
