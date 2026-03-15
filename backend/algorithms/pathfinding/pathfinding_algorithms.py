"""Pathfinding Algorithms on grids with step-by-step visualization."""
from collections import deque
import heapq, math


DIRS = [(0,1),(1,0),(0,-1),(-1,0)]


def bfs_grid(grid: list[list[int]], start: list[int], end: list[int]) -> list[dict]:
    steps = []
    rows, cols = len(grid), len(grid[0])
    visited = set()
    visited.add(tuple(start))
    queue = deque([(start[0], start[1])])
    parent = {tuple(start): None}

    while queue:
        r, c = queue.popleft()
        steps.append({"step": len(steps)+1, "current": [r, c],
                      "visited": [list(v) for v in visited],
                      "description": f"Visit ({r},{c})"})

        if r == end[0] and c == end[1]:
            path = _trace(parent, tuple(start), tuple(end))
            steps.append({"step": len(steps)+1, "path": path,
                          "visited": [list(v) for v in visited],
                          "description": f"Path found! Length={len(path)}"})
            return steps

        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0 and (nr,nc) not in visited:
                visited.add((nr,nc))
                parent[(nr,nc)] = (r,c)
                queue.append((nr,nc))

    steps.append({"step": len(steps)+1, "description": "No path found"})
    return steps


def dfs_maze(grid: list[list[int]], start: list[int], end: list[int]) -> list[dict]:
    steps = []
    rows, cols = len(grid), len(grid[0])
    visited = set()
    parent = {tuple(start): None}

    def dfs(r, c):
        visited.add((r, c))
        steps.append({"step": len(steps)+1, "current": [r, c],
                      "visited": [list(v) for v in visited],
                      "description": f"Visit ({r},{c})"})
        if r == end[0] and c == end[1]:
            return True
        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0 and (nr,nc) not in visited:
                parent[(nr,nc)] = (r,c)
                if dfs(nr, nc):
                    return True
        return False

    if dfs(start[0], start[1]):
        path = _trace(parent, tuple(start), tuple(end))
        steps.append({"step": len(steps)+1, "path": path,
                      "visited": [list(v) for v in visited],
                      "description": f"Path found! Length={len(path)}"})
    else:
        steps.append({"step": len(steps)+1, "description": "No path found"})
    return steps


def a_star_grid(grid: list[list[int]], start: list[int], end: list[int]) -> list[dict]:
    steps = []
    rows, cols = len(grid), len(grid[0])

    def h(r, c):
        return abs(r - end[0]) + abs(c - end[1])

    g = {tuple(start): 0}
    f_score = {tuple(start): h(start[0], start[1])}
    open_set = [(f_score[tuple(start)], start[0], start[1])]
    parent = {tuple(start): None}
    closed = set()

    while open_set:
        _, r, c = heapq.heappop(open_set)
        if (r, c) in closed:
            continue
        closed.add((r, c))

        steps.append({"step": len(steps)+1, "current": [r, c],
                      "visited": [list(v) for v in closed],
                      "description": f"Expand ({r},{c}) f={f_score.get((r,c),0)}"})

        if r == end[0] and c == end[1]:
            path = _trace(parent, tuple(start), tuple(end))
            steps.append({"step": len(steps)+1, "path": path,
                          "visited": [list(v) for v in closed],
                          "description": f"Path found! Cost={g[(r,c)]}"})
            return steps

        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0 and (nr,nc) not in closed:
                tentative = g[(r,c)] + 1
                if tentative < g.get((nr,nc), float('inf')):
                    g[(nr,nc)] = tentative
                    f_score[(nr,nc)] = tentative + h(nr, nc)
                    parent[(nr,nc)] = (r,c)
                    heapq.heappush(open_set, (f_score[(nr,nc)], nr, nc))

    steps.append({"step": len(steps)+1, "description": "No path found"})
    return steps


def dijkstra_grid(grid: list[list[int]], start: list[int], end: list[int]) -> list[dict]:
    steps = []
    rows, cols = len(grid), len(grid[0])
    dist = {tuple(start): 0}
    pq = [(0, start[0], start[1])]
    parent = {tuple(start): None}
    closed = set()

    while pq:
        d, r, c = heapq.heappop(pq)
        if (r,c) in closed:
            continue
        closed.add((r,c))

        steps.append({"step": len(steps)+1, "current": [r,c],
                      "visited": [list(v) for v in closed],
                      "description": f"Process ({r},{c}) dist={d}"})

        if r == end[0] and c == end[1]:
            path = _trace(parent, tuple(start), tuple(end))
            steps.append({"step": len(steps)+1, "path": path,
                          "visited": [list(v) for v in closed],
                          "description": f"Path found! Cost={d}"})
            return steps

        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0 and (nr,nc) not in closed:
                nd = d + 1
                if nd < dist.get((nr,nc), float('inf')):
                    dist[(nr,nc)] = nd
                    parent[(nr,nc)] = (r,c)
                    heapq.heappush(pq, (nd, nr, nc))

    steps.append({"step": len(steps)+1, "description": "No path found"})
    return steps


def greedy_best_first(grid: list[list[int]], start: list[int], end: list[int]) -> list[dict]:
    steps = []
    rows, cols = len(grid), len(grid[0])

    def h(r, c):
        return abs(r - end[0]) + abs(c - end[1])

    open_set = [(h(start[0], start[1]), start[0], start[1])]
    parent = {tuple(start): None}
    closed = set()

    while open_set:
        _, r, c = heapq.heappop(open_set)
        if (r,c) in closed:
            continue
        closed.add((r,c))

        steps.append({"step": len(steps)+1, "current": [r,c],
                      "visited": [list(v) for v in closed],
                      "description": f"Expand ({r},{c}) h={h(r,c)}"})

        if r == end[0] and c == end[1]:
            path = _trace(parent, tuple(start), tuple(end))
            steps.append({"step": len(steps)+1, "path": path,
                          "visited": [list(v) for v in closed],
                          "description": f"Path found!"})
            return steps

        for dr, dc in DIRS:
            nr, nc = r+dr, c+dc
            if 0<=nr<rows and 0<=nc<cols and grid[nr][nc]==0 and (nr,nc) not in closed:
                if (nr,nc) not in {(o[1],o[2]) for o in open_set}:
                    parent[(nr,nc)] = (r,c)
                    heapq.heappush(open_set, (h(nr,nc), nr, nc))

    steps.append({"step": len(steps)+1, "description": "No path found"})
    return steps


def _trace(parent, start, end):
    path = []
    cur = end
    while cur is not None:
        path.append(list(cur))
        cur = parent.get(cur)
    return list(reversed(path))
