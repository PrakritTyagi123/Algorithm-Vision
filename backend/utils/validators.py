"""Utility: Input validators."""


def validate_array(arr: list, min_len: int = 1, max_len: int = 500) -> tuple[bool, str]:
    if not isinstance(arr, list):
        return False, "Input must be a list"
    if len(arr) < min_len:
        return False, f"Array must have at least {min_len} element(s)"
    if len(arr) > max_len:
        return False, f"Array must have at most {max_len} elements"
    if not all(isinstance(x, (int, float)) for x in arr):
        return False, "All elements must be numbers"
    return True, ""


def validate_graph(nodes: list, edges: list) -> tuple[bool, str]:
    if not nodes:
        return False, "Graph must have at least one node"
    node_ids = {n["id"] for n in nodes}
    for e in edges:
        if e["from"] not in node_ids or e["to"] not in node_ids:
            return False, f"Edge references unknown node"
    return True, ""


def validate_grid(grid: list) -> tuple[bool, str]:
    if not grid or not grid[0]:
        return False, "Grid cannot be empty"
    cols = len(grid[0])
    for row in grid:
        if len(row) != cols:
            return False, "All rows must have equal length"
    return True, ""
