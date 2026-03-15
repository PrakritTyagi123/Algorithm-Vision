"""Missing Backtracking Algorithms with step-by-step visualization."""


def graph_coloring(adj: dict, node_count: int, num_colors: int = 3) -> list[dict]:
    steps = []
    colors = [-1] * node_count
    color_names = ["R", "G", "B", "Y", "P"]

    def is_safe(node, c):
        for neighbor, _ in adj.get(node, []):
            if colors[neighbor] == c:
                return False
        return True

    def _arr():
        return [c if c >= 0 else 0 for c in colors]

    def solve(node):
        if node == node_count:
            steps.append({
                "step": len(steps) + 1,
                "array": _arr(),
                "sorted": list(range(node_count)),
                "description": f"Solution: {[color_names[c] if c >= 0 else '?' for c in colors]}",
            })
            return True

        for c in range(num_colors):
            steps.append({
                "step": len(steps) + 1,
                "array": _arr(),
                "current": node,
                "description": f"Try color {color_names[c]} for node {node}",
            })

            if is_safe(node, c):
                colors[node] = c
                steps.append({
                    "step": len(steps) + 1,
                    "array": _arr(),
                    "active": [i for i in range(node_count) if colors[i] >= 0],
                    "description": f"Assign {color_names[c]} to node {node}",
                })
                if solve(node + 1):
                    return True
                colors[node] = -1
                steps.append({
                    "step": len(steps) + 1,
                    "array": _arr(),
                    "swap": [node],
                    "description": f"Backtrack: uncolor node {node}",
                })

        return False

    if not solve(0):
        steps.append({"step": len(steps) + 1, "array": _arr(),
                      "description": f"No {num_colors}-coloring exists"})
    return steps


def rat_in_maze(maze: list[list[int]]) -> list[dict]:
    steps = []
    n = len(maze)
    solution = [[0] * n for _ in range(n)]

    def is_safe(r, c):
        return 0 <= r < n and 0 <= c < n and maze[r][c] == 1

    def solve(r, c):
        if r == n - 1 and c == n - 1:
            solution[r][c] = 1
            placed = [[i, j] for i in range(n) for j in range(n) if solution[i][j] == 1]
            steps.append({"step": len(steps) + 1,
                          "board": [row[:] for row in solution],
                          "current": [r, c], "placed": placed,
                          "description": f"Reached destination ({r},{c})!"})
            return True

        if is_safe(r, c):
            solution[r][c] = 1
            placed = [[i, j] for i in range(n) for j in range(n) if solution[i][j] == 1]
            steps.append({"step": len(steps) + 1,
                          "board": [row[:] for row in solution],
                          "current": [r, c], "placed": placed,
                          "description": f"Move to ({r},{c})"})

            if solve(r + 1, c):
                return True
            if solve(r, c + 1):
                return True

            solution[r][c] = 0
            steps.append({"step": len(steps) + 1,
                          "board": [row[:] for row in solution],
                          "conflict": [[r, c]],
                          "description": f"Backtrack from ({r},{c})"})

        return False

    if not solve(0, 0):
        steps.append({"step": len(steps) + 1, "description": "No path exists"})
    return steps


def word_search(board: list[list[str]], word: str) -> list[dict]:
    steps = []
    if not board or not board[0]:
        return steps
    rows, cols = len(board), len(board[0])
    visited = set()

    def dfs(r, c, idx):
        if idx == len(word):
            steps.append({"step": len(steps) + 1,
                          "board": [row[:] for row in board],
                          "placed": [list(v) for v in visited],
                          "description": f"Word '{word}' found!"})
            return True

        if r < 0 or r >= rows or c < 0 or c >= cols:
            return False
        if (r, c) in visited or board[r][c] != word[idx]:
            return False

        visited.add((r, c))
        steps.append({"step": len(steps) + 1,
                      "board": [row[:] for row in board],
                      "current": [r, c],
                      "placed": [list(v) for v in visited],
                      "description": f"Match '{word[idx]}' at ({r},{c}), progress: {word[:idx+1]}"})

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if dfs(r + dr, c + dc, idx + 1):
                return True

        visited.discard((r, c))
        steps.append({"step": len(steps) + 1,
                      "board": [row[:] for row in board],
                      "conflict": [[r, c]],
                      "description": f"Backtrack from ({r},{c})"})
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if dfs(r, c, 0):
                    return steps

    steps.append({"step": len(steps) + 1, "description": f"Word '{word}' not found"})
    return steps
