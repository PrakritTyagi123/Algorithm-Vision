"""A* Search — O(E) time (heuristic-dependent), O(V) space"""
import heapq, math


def a_star(adj: dict, nodes: list[dict], start: int, end: int) -> list[dict]:
    steps = []
    if end is None:
        return steps

    def heuristic(a, b):
        na, nb = nodes[a], nodes[b]
        return math.sqrt((na["x"]-nb["x"])**2 + (na["y"]-nb["y"])**2)

    g = {start: 0}
    f = {start: heuristic(start, end)}
    parent = {start: None}
    open_set = [(f[start], start)]
    closed = set()

    while open_set:
        _, u = heapq.heappop(open_set)
        if u in closed:
            continue
        closed.add(u)

        steps.append({
            "step": len(steps)+1, "current": u,
            "visited": list(closed),
            "start_node": start, "end_node": end,
            "distances": {str(k): round(v, 1) for k, v in g.items()},
            "description": f"Expand {u} (g={g[u]:.1f}, f={f.get(u,0):.1f})",
        })

        if u == end:
            path = []
            cur = end
            while cur is not None:
                path.append(cur)
                cur = parent.get(cur)
            path.reverse()
            steps.append({"step": len(steps)+1, "visited": list(closed),
                          "path": path, "start_node": start, "end_node": end,
                          "description": f"Path found! Cost={g[end]:.1f}"})
            return steps

        for v, w in adj.get(u, []):
            if v in closed:
                continue
            tentative = g[u] + w
            if tentative < g.get(v, float('inf')):
                g[v] = tentative
                f[v] = tentative + heuristic(v, end)
                parent[v] = u
                heapq.heappush(open_set, (f[v], v))
                steps.append({
                    "step": len(steps)+1, "current": u,
                    "visited": list(closed), "edge_active": [u, v],
                    "start_node": start, "end_node": end,
                    "description": f"Relax {u}→{v}: g={tentative:.1f}",
                })

    steps.append({"step": len(steps)+1, "description": f"No path to {end}"})
    return steps
