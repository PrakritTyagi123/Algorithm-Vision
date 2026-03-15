"""Missing DP Algorithms with step-by-step visualization."""


def longest_palindromic_subsequence(text: str) -> list[dict]:
    steps = []
    n = len(text)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = 1

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if text[i] == text[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2 if length > 2 else 2
                desc = f"Match '{text[i]}': dp[{i}][{j}] = {dp[i][j]}"
                hl = [[i + 1, j - 1]] if length > 2 else []
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
                desc = f"No match: dp[{i}][{j}] = max({dp[i+1][j]}, {dp[i][j-1]}) = {dp[i][j]}"
                hl = [[i + 1, j], [i, j - 1]]

            steps.append({
                "step": len(steps) + 1,
                "table": [row[:] for row in dp],
                "row_headers": list(text), "col_headers": list(text),
                "current": [i, j], "highlighted": hl,
                "description": desc,
            })

    steps.append({"step": len(steps) + 1,
                  "table": [row[:] for row in dp],
                  "row_headers": list(text), "col_headers": list(text),
                  "description": f"Longest palindromic subsequence length = {dp[0][n-1]}"})
    return steps


def minimum_path_sum(grid: list[list[int]]) -> list[dict]:
    steps = []
    rows, cols = len(grid), len(grid[0])
    dp = [[0] * cols for _ in range(rows)]
    dp[0][0] = grid[0][0]

    for i in range(1, rows):
        dp[i][0] = dp[i - 1][0] + grid[i][0]
    for j in range(1, cols):
        dp[0][j] = dp[0][j - 1] + grid[0][j]

    for i in range(1, rows):
        for j in range(1, cols):
            dp[i][j] = grid[i][j] + min(dp[i - 1][j], dp[i][j - 1])
            steps.append({
                "step": len(steps) + 1,
                "table": [row[:] for row in dp],
                "current": [i, j],
                "highlighted": [[i - 1, j], [i, j - 1]],
                "description": f"dp[{i}][{j}] = {grid[i][j]} + min({dp[i-1][j]}, {dp[i][j-1]}) = {dp[i][j]}",
            })

    # Trace path
    path = []
    i, j = rows - 1, cols - 1
    path.append([i, j])
    while i > 0 or j > 0:
        if i == 0:
            j -= 1
        elif j == 0:
            i -= 1
        elif dp[i - 1][j] < dp[i][j - 1]:
            i -= 1
        else:
            j -= 1
        path.append([i, j])
    path.reverse()

    steps.append({"step": len(steps) + 1,
                  "table": [row[:] for row in dp], "path": path,
                  "description": f"Min path sum = {dp[rows-1][cols-1]}"})
    return steps


def partition_equal_subset_sum(nums: list[int]) -> list[dict]:
    steps = []
    total = sum(nums)

    if total % 2 != 0:
        steps.append({"step": 1, "description": f"Sum={total} is odd — cannot partition equally"})
        return steps

    target = total // 2
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    for i in range(n + 1):
        dp[i][0] = True

    for i in range(1, n + 1):
        for j in range(1, target + 1):
            dp[i][j] = dp[i - 1][j]
            if nums[i - 1] <= j:
                dp[i][j] = dp[i][j] or dp[i - 1][j - nums[i - 1]]

            steps.append({
                "step": len(steps) + 1,
                "table": [[1 if c else 0 for c in row] for row in dp],
                "row_headers": ["0"] + [str(x) for x in nums],
                "col_headers": [str(j2) for j2 in range(target + 1)],
                "current": [i, j],
                "description": f"dp[{i}][{j}] = {dp[i][j]} (num={nums[i-1]})",
            })

    result = dp[n][target]
    steps.append({"step": len(steps) + 1,
                  "description": f"Can partition into two equal subsets: {'Yes' if result else 'No'}"})
    return steps


def traveling_salesman_dp(dist_matrix: list[list[int]]) -> list[dict]:
    steps = []
    n = len(dist_matrix)
    INF = 999999
    dp = [[INF] * n for _ in range(1 << n)]
    parent = [[(-1, -1)] * n for _ in range(1 << n)]
    dp[1][0] = 0

    # Show distance matrix
    steps.append({
        "step": len(steps) + 1,
        "table": dist_matrix,
        "row_headers": [str(i) for i in range(n)],
        "col_headers": [str(i) for i in range(n)],
        "description": f"TSP with {n} cities. Distance matrix shown.",
    })

    # Build summary table: best cost to reach each city so far
    best = [INF] * n
    best[0] = 0

    for mask in range(1 << n):
        for u in range(n):
            if dp[mask][u] == INF or not (mask & (1 << u)):
                continue
            for v in range(n):
                if mask & (1 << v):
                    continue
                new_mask = mask | (1 << v)
                new_cost = dp[mask][u] + dist_matrix[u][v]
                if new_cost < dp[new_mask][v]:
                    dp[new_mask][v] = new_cost
                    parent[new_mask][v] = (mask, u)
                    if new_cost < best[v]:
                        best[v] = new_cost
                    steps.append({
                        "step": len(steps) + 1,
                        "table": [[b if b < INF else -1 for b in best]],
                        "col_headers": [f"city {i}" for i in range(n)],
                        "current": [0, v],
                        "highlighted": [[0, u]],
                        "description": f"Visit {v} from {u}: cost={new_cost}",
                    })

    full_mask = (1 << n) - 1
    min_cost = INF
    last = -1
    for u in range(n):
        total = dp[full_mask][u] + dist_matrix[u][0]
        if total < min_cost:
            min_cost = total
            last = u

    path = [0]
    mask = full_mask
    cur = last
    while cur != 0 or mask != 1:
        path.append(cur)
        prev_mask, prev_node = parent[mask][cur]
        mask, cur = prev_mask, prev_node
    path.append(0)
    path.reverse()

    steps.append({
        "step": len(steps) + 1,
        "table": dist_matrix,
        "row_headers": [str(i) for i in range(n)],
        "col_headers": [str(i) for i in range(n)],
        "path": path,
        "description": f"Optimal tour: {' → '.join(map(str, path))}, cost={min_cost}",
    })
    return steps
