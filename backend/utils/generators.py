"""Utility: Random data generators for testing."""
import random


def random_array(size: int = 30, lo: int = 1, hi: int = 100) -> list[int]:
    return [random.randint(lo, hi) for _ in range(size)]


def random_sorted_array(size: int = 30, lo: int = 1, hi: int = 100) -> list[int]:
    return sorted(random_array(size, lo, hi))


def random_graph(node_count: int = 8, density: float = 0.4, directed: bool = False):
    import math
    nodes = []
    edges = []
    cx, cy, r = 400, 300, 200
    for i in range(node_count):
        angle = 2 * math.pi * i / node_count - math.pi / 2
        nodes.append({"id": i, "label": chr(65 + i),
                      "x": cx + r * math.cos(angle), "y": cy + r * math.sin(angle)})
    for i in range(node_count):
        for j in range(i + 1, node_count):
            if random.random() < density:
                w = random.randint(1, 20)
                edges.append({"from": i, "to": j, "weight": w})
                if not directed:
                    edges.append({"from": j, "to": i, "weight": w})
    return {"nodes": nodes, "edges": edges}


def random_grid(rows: int = 20, cols: int = 30, wall_ratio: float = 0.25):
    grid = [[1 if random.random() < wall_ratio else 0 for _ in range(cols)] for _ in range(rows)]
    grid[1][1] = 0
    grid[rows-2][cols-2] = 0
    return {"grid": grid, "start": [1, 1], "end": [rows-2, cols-2]}
