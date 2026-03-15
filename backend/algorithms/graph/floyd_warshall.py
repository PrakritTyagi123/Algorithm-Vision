"""Floyd-Warshall — O(V³) time, O(V²) space. All-pairs shortest path."""


def floyd_warshall(adj: dict, node_count: int) -> list[dict]:
    INF = float('inf')
    dist = [[INF]*node_count for _ in range(node_count)]
    steps = []

    for i in range(node_count):
        dist[i][i] = 0
    for u in adj:
        for v, w in adj[u]:
            dist[u][v] = w

    for k in range(node_count):
        for i in range(node_count):
            for j in range(node_count):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    steps.append({
                        "step": len(steps)+1,
                        "table": [[v if v != INF else -1 for v in row] for row in dist],
                        "current": [i, j],
                        "highlighted": [[i, k], [k, j]],
                        "description": f"Via {k}: dist[{i}][{j}] = {dist[i][j]}",
                    })

    steps.append({
        "step": len(steps)+1,
        "table": [[v if v != INF else -1 for v in row] for row in dist],
        "description": "Floyd-Warshall complete",
    })
    return steps
