"""Backtracking Algorithms with step-by-step visualization."""


def n_queens(n: int) -> list[dict]:
    steps = []
    board = [[0]*n for _ in range(n)]
    placed = []

    def is_safe(row, col):
        for r, c in placed:
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def solve(row):
        if row == n:
            steps.append({"step": len(steps)+1,
                          "board": [["♛" if cell else "" for cell in r] for r in board],
                          "placed": [list(p) for p in placed],
                          "description": "Solution found!"})
            return True
        for col in range(n):
            steps.append({"step": len(steps)+1,
                          "board": [["♛" if cell else "" for cell in r] for r in board],
                          "current": [row, col], "placed": [list(p) for p in placed],
                          "description": f"Try queen at ({row}, {col})"})
            if is_safe(row, col):
                board[row][col] = 1
                placed.append((row, col))
                steps.append({"step": len(steps)+1,
                              "board": [["♛" if cell else "" for cell in r] for r in board],
                              "placed": [list(p) for p in placed],
                              "description": f"Place queen at ({row}, {col})"})
                if solve(row + 1):
                    return True
                board[row][col] = 0
                placed.pop()
                steps.append({"step": len(steps)+1,
                              "board": [["♛" if cell else "" for cell in r] for r in board],
                              "conflict": [[row, col]], "placed": [list(p) for p in placed],
                              "description": f"Backtrack from ({row}, {col})"})
        return False

    solve(0)
    return steps


def sudoku_solver(board_input: list[list[int]]) -> list[dict]:
    board = [row[:] for row in board_input]
    steps = []

    def is_valid(r, c, num):
        for i in range(9):
            if board[r][i] == num or board[i][c] == num:
                return False
        br, bc = 3*(r//3), 3*(c//3)
        for i in range(br, br+3):
            for j in range(bc, bc+3):
                if board[i][j] == num:
                    return False
        return True

    def solve():
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    for num in range(1, 10):
                        steps.append({"step": len(steps)+1,
                                      "board": [row[:] for row in board],
                                      "current": [r, c],
                                      "description": f"Try {num} at ({r},{c})"})
                        if is_valid(r, c, num):
                            board[r][c] = num
                            steps.append({"step": len(steps)+1,
                                          "board": [row[:] for row in board],
                                          "placed": [[r, c]],
                                          "description": f"Place {num} at ({r},{c})"})
                            if solve():
                                return True
                            board[r][c] = 0
                            steps.append({"step": len(steps)+1,
                                          "board": [row[:] for row in board],
                                          "conflict": [[r, c]],
                                          "description": f"Backtrack ({r},{c})"})
                    return False
        steps.append({"step": len(steps)+1, "board": [row[:] for row in board],
                      "description": "Sudoku solved!"})
        return True

    solve()
    return steps


def knights_tour(n: int) -> list[dict]:
    board = [[-1]*n for _ in range(n)]
    steps = []
    moves = [(2,1),(1,2),(-1,2),(-2,1),(-2,-1),(-1,-2),(1,-2),(2,-1)]

    def solve(x, y, move_num):
        board[x][y] = move_num
        placed = [[r, c] for r in range(n) for c in range(n) if board[r][c] >= 0]
        steps.append({"step": len(steps)+1,
                      "board": [[cell if cell >= 0 else "" for cell in row] for row in board],
                      "current": [x, y], "placed": placed,
                      "description": f"Move {move_num}: knight at ({x},{y})"})

        if move_num == n*n - 1:
            return True

        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < n and 0 <= ny < n and board[nx][ny] == -1:
                if solve(nx, ny, move_num + 1):
                    return True

        board[x][y] = -1
        steps.append({"step": len(steps)+1,
                      "board": [[cell if cell >= 0 else "" for cell in row] for row in board],
                      "conflict": [[x, y]],
                      "description": f"Backtrack from ({x},{y})"})
        return False

    solve(0, 0, 0)
    return steps


def subset_sum(values: list[int], target: int) -> list[dict]:
    steps = []
    n = len(values)

    def solve(idx, current_sum, subset):
        if current_sum == target:
            steps.append({"step": len(steps)+1,
                          "array": values, "active": list(subset),
                          "found": list(subset),
                          "description": f"Found subset: {[values[i] for i in subset]} = {target}"})
            return True
        if idx == n or current_sum > target:
            return False

        # Include
        subset.append(idx)
        steps.append({"step": len(steps)+1, "array": values, "active": list(subset),
                      "current": idx, "description": f"Include {values[idx]}, sum={current_sum+values[idx]}"})
        if solve(idx + 1, current_sum + values[idx], subset):
            return True
        subset.pop()

        # Exclude
        steps.append({"step": len(steps)+1, "array": values, "active": list(subset),
                      "current": idx, "description": f"Exclude {values[idx]}"})
        return solve(idx + 1, current_sum, subset)

    solve(0, 0, [])
    return steps


def permutations(values: list[int]) -> list[dict]:
    steps = []
    a = list(values)
    n = len(a)

    def permute(start):
        if start == n:
            steps.append({"step": len(steps)+1, "array": list(a),
                          "sorted": list(range(n)),
                          "description": f"Permutation: {list(a)}"})
            return
        for i in range(start, n):
            a[start], a[i] = a[i], a[start]
            steps.append({"step": len(steps)+1, "array": list(a), "swap": [start, i],
                          "description": f"Swap index {start} ↔ {i}"})
            permute(start + 1)
            a[start], a[i] = a[i], a[start]

    permute(0)
    return steps


def combinations(values: list[int], k: int) -> list[dict]:
    steps = []
    n = len(values)

    def combine(start, combo):
        if len(combo) == k:
            steps.append({"step": len(steps)+1, "array": values,
                          "active": list(combo),
                          "description": f"Combination: {[values[i] for i in combo]}"})
            return
        for i in range(start, n):
            combo.append(i)
            steps.append({"step": len(steps)+1, "array": values, "active": list(combo),
                          "current": i, "description": f"Add {values[i]}"})
            combine(i + 1, combo)
            combo.pop()

    combine(0, [])
    return steps
