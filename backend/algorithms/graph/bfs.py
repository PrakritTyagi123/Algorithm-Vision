"""Breadth-First Search — O(V+E) time, O(V) space"""
from collections import deque


def bfs(adj: dict, start: int, end: int = None) -> list[dict]:
    steps = []
    visited = set()
    queue = deque([start])
    visited.add(start)
    parent = {start: None}

    while queue:
        node = queue.popleft()
        steps.append({
            "step": len(steps)+1, "current": node,
            "visited": list(visited), "frontier": list(queue),
            "description": f"Visit node {node}",
        })

        if end is not None and node == end:
            path = _reconstruct(parent, start, end)
            steps.append({"step": len(steps)+1, "visited": list(visited),
                          "path": path, "description": f"Found path to {end}!"})
            return steps

        for neighbor, _ in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                queue.append(neighbor)
                steps.append({
                    "step": len(steps)+1, "current": node,
                    "visited": list(visited), "frontier": list(queue),
                    "edge_active": [node, neighbor],
                    "description": f"Discover {neighbor} from {node}",
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
