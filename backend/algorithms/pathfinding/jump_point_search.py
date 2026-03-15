"""Jump Point Search — optimized A* for uniform-cost grids — O(E) time"""
import heapq


DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def jump_point_search(grid: list[list[int]], start: list[int], end: list[int]) -> list[dict]:
    steps = []
    rows, cols = len(grid), len(grid[0])

    def blocked(r, c):
        return r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == 1

    def h(r, c):
        return abs(r - end[0]) + abs(c - end[1])

    def jump(r, c, dr, dc):
        nr, nc = r + dr, c + dc
        if blocked(nr, nc):
            return None

        steps.append({
            "step": len(steps) + 1,
            "current": [nr, nc],
            "visited": [list(v) for v in closed],
            "description": f"Jump from ({r},{c}) dir=({dr},{dc}) → ({nr},{nc})",
        })

        if nr == end[0] and nc == end[1]:
            return (nr, nc)

        # Diagonal movement
        if dr != 0 and dc != 0:
            # Forced neighbors check
            if (blocked(nr - dr, nc) and not blocked(nr - dr, nc + dc)) or \
               (blocked(nr, nc - dc) and not blocked(nr + dr, nc - dc)):
                return (nr, nc)
            # Recursive cardinal jumps
            if jump(nr, nc, dr, 0) is not None or jump(nr, nc, 0, dc) is not None:
                return (nr, nc)
        else:
            # Cardinal movement
            if dr != 0:
                if (not blocked(nr, nc + 1) and blocked(nr - dr, nc + 1)) or \
                   (not blocked(nr, nc - 1) and blocked(nr - dr, nc - 1)):
                    return (nr, nc)
            else:
                if (not blocked(nr + 1, nc) and blocked(nr + 1, nc - dc)) or \
                   (not blocked(nr - 1, nc) and blocked(nr - 1, nc - dc)):
                    return (nr, nc)

        return jump(nr, nc, dr, dc)

    g = {(start[0], start[1]): 0}
    open_set = [(h(start[0], start[1]), start[0], start[1])]
    parent = {(start[0], start[1]): None}
    closed = set()

    while open_set:
        _, r, c = heapq.heappop(open_set)
        if (r, c) in closed:
            continue
        closed.add((r, c))

        if r == end[0] and c == end[1]:
            path = _trace(parent, tuple(start), tuple(end))
            steps.append({"step": len(steps) + 1, "path": path,
                          "visited": [list(v) for v in closed],
                          "description": f"Path found! Length={len(path)}"})
            return steps

        for dr, dc in DIRS:
            jp = jump(r, c, dr, dc)
            if jp is not None:
                nr, nc = jp
                dist = abs(nr - r) + abs(nc - c)
                ng = g[(r, c)] + dist
                if ng < g.get((nr, nc), float('inf')):
                    g[(nr, nc)] = ng
                    parent[(nr, nc)] = (r, c)
                    heapq.heappush(open_set, (ng + h(nr, nc), nr, nc))

    steps.append({"step": len(steps) + 1, "description": "No path found"})
    return steps


def _trace(parent, start, end):
    """Trace back jump points, then interpolate cells between each pair."""
    # Get jump points
    jump_pts = []
    cur = end
    while cur is not None:
        jump_pts.append(cur)
        cur = parent.get(cur)
    jump_pts.reverse()

    # Interpolate cells between consecutive jump points
    if len(jump_pts) <= 1:
        return [list(p) for p in jump_pts]

    full_path = []
    for i in range(len(jump_pts) - 1):
        r1, c1 = jump_pts[i]
        r2, c2 = jump_pts[i + 1]
        # Walk from (r1,c1) to (r2,c2) step by step
        dr = 0 if r2 == r1 else (1 if r2 > r1 else -1)
        dc = 0 if c2 == c1 else (1 if c2 > c1 else -1)
        r, c = r1, c1
        while r != r2 or c != c2:
            if [r, c] not in full_path:
                full_path.append([r, c])
            if r != r2:
                r += dr
            if c != c2:
                c += dc
    full_path.append([jump_pts[-1][0], jump_pts[-1][1]])
    return full_path
