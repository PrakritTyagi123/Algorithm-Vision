"""Computational Geometry Algorithms with step-by-step visualization."""
import math


def convex_hull_graham(points: list[list[int]]) -> list[dict]:
    steps = []
    pts = [tuple(p) for p in points]
    n = len(pts)
    if n < 3:
        steps.append({"step": 1, "description": "Need at least 3 points"})
        return steps

    # Find lowest point (and leftmost if tie)
    pivot = min(pts, key=lambda p: (p[1], p[0]))
    steps.append({"step": len(steps) + 1,
                  "description": f"Pivot (lowest point): {pivot}"})

    def polar_angle(p):
        return math.atan2(p[1] - pivot[1], p[0] - pivot[0])

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    sorted_pts = sorted(pts, key=lambda p: (polar_angle(p), -((p[0]-pivot[0])**2 + (p[1]-pivot[1])**2)))

    steps.append({"step": len(steps) + 1,
                  "description": f"Points sorted by polar angle from pivot"})

    stack = [sorted_pts[0], sorted_pts[1]]

    for i in range(2, n):
        while len(stack) > 1 and cross(stack[-2], stack[-1], sorted_pts[i]) <= 0:
            removed = stack.pop()
            steps.append({"step": len(steps) + 1,
                          "description": f"Remove {removed} (not left turn)"})

        stack.append(sorted_pts[i])
        steps.append({"step": len(steps) + 1,
                      "path": [list(p) for p in stack],
                      "description": f"Add {sorted_pts[i]} to hull"})

    hull = [list(p) for p in stack]
    steps.append({"step": len(steps) + 1,
                  "path": hull + [hull[0]],
                  "description": f"Convex hull has {len(hull)} vertices"})
    return steps


def convex_hull_jarvis(points: list[list[int]]) -> list[dict]:
    steps = []
    pts = [tuple(p) for p in points]
    n = len(pts)
    if n < 3:
        steps.append({"step": 1, "description": "Need at least 3 points"})
        return steps

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    # Start from leftmost
    start = min(pts, key=lambda p: (p[0], p[1]))
    hull = []
    current = start

    while True:
        hull.append(current)
        steps.append({"step": len(steps) + 1,
                      "path": [list(p) for p in hull],
                      "description": f"Add {current} to hull"})

        candidate = pts[0]
        for p in pts[1:]:
            if candidate == current or cross(current, candidate, p) < 0:
                candidate = p
                steps.append({"step": len(steps) + 1,
                              "edge_active": [pts.index(current), pts.index(p)],
                              "description": f"Better candidate: {p}"})

        current = candidate
        if current == start:
            break

    hull_list = [list(p) for p in hull]
    steps.append({"step": len(steps) + 1,
                  "path": hull_list + [hull_list[0]],
                  "description": f"Jarvis march complete: {len(hull)} vertices"})
    return steps


def closest_pair_of_points(points: list[list[int]]) -> list[dict]:
    steps = []
    pts = [tuple(p) for p in points]

    def dist(a, b):
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)

    n = len(pts)
    if n < 2:
        steps.append({"step": 1, "description": "Need at least 2 points"})
        return steps

    sorted_pts = sorted(pts, key=lambda p: p[0])
    min_dist = float('inf')
    best_pair = None

    def solve(left, right):
        nonlocal min_dist, best_pair

        if right - left < 3:
            for i in range(left, right):
                for j in range(i + 1, right):
                    d = dist(sorted_pts[i], sorted_pts[j])
                    steps.append({"step": len(steps) + 1,
                                  "edge_active": [i, j],
                                  "description": f"Brute: d({sorted_pts[i]}, {sorted_pts[j]}) = {d:.2f}"})
                    if d < min_dist:
                        min_dist = d
                        best_pair = (sorted_pts[i], sorted_pts[j])
            return

        mid = (left + right) // 2
        mid_x = sorted_pts[mid][0]

        steps.append({"step": len(steps) + 1,
                      "description": f"Divide at x={mid_x} (indices {left}..{right})"})

        solve(left, mid)
        solve(mid, right)

        # Check strip
        strip = [p for p in sorted_pts[left:right] if abs(p[0] - mid_x) < min_dist]
        strip.sort(key=lambda p: p[1])

        for i in range(len(strip)):
            j = i + 1
            while j < len(strip) and strip[j][1] - strip[i][1] < min_dist:
                d = dist(strip[i], strip[j])
                if d < min_dist:
                    min_dist = d
                    best_pair = (strip[i], strip[j])
                    steps.append({"step": len(steps) + 1,
                                  "description": f"Strip: new min d({strip[i]}, {strip[j]}) = {d:.2f}"})
                j += 1

    solve(0, n)

    if best_pair:
        steps.append({"step": len(steps) + 1,
                      "description": f"Closest pair: {best_pair[0]} and {best_pair[1]}, distance = {min_dist:.4f}"})
    return steps
