"""Depth-First Search — O(V+E) time, O(V) space"""


def dfs(adj: dict, start: int, end: int = None) -> list[dict]:
    steps = []
    visited = set()
    parent = {start: None}
    found = [False]

    def _dfs(node):
        if found[0]:
            return
        visited.add(node)
        steps.append({
            "step": len(steps)+1, "current": node,
            "visited": list(visited),
            "description": f"Visit node {node}",
        })

        if end is not None and node == end:
            path = _reconstruct(parent, start, end)
            steps.append({"step": len(steps)+1, "visited": list(visited),
                          "path": path, "description": f"Found path to {end}!"})
            found[0] = True
            return

        for neighbor, _ in adj.get(node, []):
            if neighbor not in visited:
                parent[neighbor] = node
                steps.append({
                    "step": len(steps)+1, "current": node,
                    "visited": list(visited),
                    "edge_active": [node, neighbor],
                    "description": f"Explore {node} → {neighbor}",
                })
                _dfs(neighbor)

    _dfs(start)
    return steps


def _reconstruct(parent, start, end):
    path = []
    cur = end
    while cur is not None:
        path.append(cur)
        cur = parent.get(cur)
    return list(reversed(path))
