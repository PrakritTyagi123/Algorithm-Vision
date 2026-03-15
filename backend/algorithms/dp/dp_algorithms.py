"""Dynamic Programming Algorithms with step-by-step visualization."""


def fibonacci_dp(n: int) -> list[dict]:
    steps = []
    dp = [0] * (n + 1)
    if n >= 1:
        dp[1] = 1
    headers = [str(i) for i in range(n + 1)]

    for i in range(2, n + 1):
        dp[i] = dp[i-1] + dp[i-2]
        steps.append({
            "step": len(steps)+1,
            "table": [dp[:i+1] + [None]*(n-i)],
            "col_headers": headers,
            "current": [0, i],
            "highlighted": [[0, i-1], [0, i-2]],
            "description": f"dp[{i}] = dp[{i-1}] + dp[{i-2}] = {dp[i]}",
        })

    steps.append({"step": len(steps)+1, "table": [dp], "col_headers": headers,
                  "description": f"Fibonacci({n}) = {dp[n]}"})
    return steps


def knapsack(weights: list[int], profits: list[int], capacity: int) -> list[dict]:
    n = len(weights)
    steps = []
    dp = [[0]*(capacity+1) for _ in range(n+1)]
    row_h = ["0"] + [f"item{i}" for i in range(1, n+1)]
    col_h = [str(c) for c in range(capacity+1)]

    for i in range(1, n+1):
        for w in range(1, capacity+1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], profits[i-1] + dp[i-1][w - weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]

            steps.append({
                "step": len(steps)+1,
                "table": [row[:] for row in dp],
                "row_headers": row_h, "col_headers": col_h,
                "current": [i, w],
                "highlighted": [[i-1, w]] + ([[i-1, w-weights[i-1]]] if weights[i-1] <= w else []),
                "description": f"dp[{i}][{w}] = {dp[i][w]}",
            })

    steps.append({"step": len(steps)+1, "table": [row[:] for row in dp],
                  "row_headers": row_h, "col_headers": col_h,
                  "description": f"Max profit = {dp[n][capacity]}"})
    return steps


def lcs(text1: str, text2: str) -> list[dict]:
    m, n = len(text1), len(text2)
    steps = []
    dp = [[0]*(n+1) for _ in range(m+1)]
    row_h = [""] + list(text1)
    col_h = [""] + list(text2)

    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                desc = f"Match '{text1[i-1]}': dp[{i}][{j}] = {dp[i][j]}"
                hl = [[i-1, j-1]]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
                desc = f"No match: dp[{i}][{j}] = max({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}"
                hl = [[i-1, j], [i, j-1]]

            steps.append({
                "step": len(steps)+1,
                "table": [row[:] for row in dp],
                "row_headers": row_h, "col_headers": col_h,
                "current": [i, j], "highlighted": hl,
                "description": desc,
            })

    steps.append({"step": len(steps)+1, "table": [row[:] for row in dp],
                  "row_headers": row_h, "col_headers": col_h,
                  "description": f"LCS length = {dp[m][n]}"})
    return steps


def lis(arr: list[int]) -> list[dict]:
    n = len(arr)
    steps = []
    dp = [1] * n

    for i in range(1, n):
        for j in range(i):
            if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                dp[i] = dp[j] + 1
                steps.append({
                    "step": len(steps)+1,
                    "table": [dp[:]],
                    "col_headers": [str(x) for x in arr],
                    "current": [0, i], "highlighted": [[0, j]],
                    "description": f"dp[{i}] = dp[{j}]+1 = {dp[i]} (arr[{j}]={arr[j]} < arr[{i}]={arr[i]})",
                })

    result = max(dp)
    steps.append({"step": len(steps)+1, "table": [dp[:]],
                  "col_headers": [str(x) for x in arr],
                  "description": f"LIS length = {result}"})
    return steps


def coin_change(coins: list[int], amount: int) -> list[dict]:
    steps = []
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    headers = [str(i) for i in range(amount + 1)]

    def _safe_dp():
        return [[v if v != float('inf') else -1 for v in dp]]

    for i in range(1, amount + 1):
        for c in coins:
            if c <= i and dp[i - c] + 1 < dp[i]:
                dp[i] = dp[i - c] + 1
                steps.append({
                    "step": len(steps)+1,
                    "table": _safe_dp(),
                    "col_headers": headers,
                    "current": [0, i], "highlighted": [[0, i - c]],
                    "description": f"dp[{i}] = dp[{i-c}]+1 = {dp[i]} (coin={c})",
                })

    result = dp[amount] if dp[amount] != float('inf') else -1
    steps.append({"step": len(steps)+1,
                  "table": _safe_dp(),
                  "col_headers": headers,
                  "description": f"Min coins for {amount} = {result}"})
    return steps


def edit_distance(text1: str, text2: str) -> list[dict]:
    m, n = len(text1), len(text2)
    steps = []
    dp = [[0]*(n+1) for _ in range(m+1)]
    for i in range(m+1):
        dp[i][0] = i
    for j in range(n+1):
        dp[0][j] = j
    row_h = [""] + list(text1)
    col_h = [""] + list(text2)

    for i in range(1, m+1):
        for j in range(1, n+1):
            if text1[i-1] == text2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
            steps.append({
                "step": len(steps)+1,
                "table": [row[:] for row in dp],
                "row_headers": row_h, "col_headers": col_h,
                "current": [i, j],
                "description": f"dp[{i}][{j}] = {dp[i][j]}",
            })

    steps.append({"step": len(steps)+1, "table": [row[:] for row in dp],
                  "row_headers": row_h, "col_headers": col_h,
                  "description": f"Edit distance = {dp[m][n]}"})
    return steps


def rod_cutting(prices: list[int], n: int) -> list[dict]:
    steps = []
    dp = [0] * (n + 1)
    headers = [str(i) for i in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, i + 1):
            if prices[j-1] + dp[i-j] > dp[i]:
                dp[i] = prices[j-1] + dp[i-j]
                steps.append({
                    "step": len(steps)+1,
                    "table": [dp[:]],
                    "col_headers": headers,
                    "current": [0, i], "highlighted": [[0, i-j]],
                    "description": f"dp[{i}] = price[{j}] + dp[{i-j}] = {dp[i]}",
                })

    steps.append({"step": len(steps)+1, "table": [dp[:]], "col_headers": headers,
                  "description": f"Max revenue for rod of length {n} = {dp[n]}"})
    return steps


def matrix_chain(dims: list[int]) -> list[dict]:
    n = len(dims) - 1
    steps = []
    dp = [[0]*n for _ in range(n)]
    headers = [f"M{i+1}" for i in range(n)]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + dims[i]*dims[k+1]*dims[j+1]
                if cost < dp[i][j]:
                    dp[i][j] = cost
                    steps.append({
                        "step": len(steps)+1,
                        "table": [[v if v != float('inf') and v != 0 else None for v in row] for row in dp],
                        "row_headers": headers, "col_headers": headers,
                        "current": [i, j], "highlighted": [[i, k], [k+1, j]],
                        "description": f"dp[{i}][{j}] = {cost} (split at k={k})",
                    })

    steps.append({"step": len(steps)+1,
                  "table": [[v if v else None for v in row] for row in dp],
                  "row_headers": headers, "col_headers": headers,
                  "description": f"Min multiplications = {dp[0][n-1]}"})
    return steps
