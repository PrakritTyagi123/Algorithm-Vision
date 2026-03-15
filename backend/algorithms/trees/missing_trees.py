"""Missing Tree Algorithms: LCA, Height, Diameter with step visualization."""


def _build_bst(values):
    root = None
    for v in values:
        root = _insert(root, v)
    return root


def _insert(node, val):
    if not node:
        return {"value": val, "left": None, "right": None}
    if val < node["value"]:
        node["left"] = _insert(node["left"], val)
    elif val > node["value"]:
        node["right"] = _insert(node["right"], val)
    return node


def _to_dict(node):
    if not node:
        return None
    return {"value": node["value"], "left": _to_dict(node.get("left")),
            "right": _to_dict(node.get("right"))}


def lowest_common_ancestor(values: list[int], a: int, b: int) -> list[dict]:
    root = _build_bst(values)
    steps = []
    steps.append({"step": 1, "tree": _to_dict(root),
                  "description": f"Find LCA of {a} and {b}"})

    node = root
    visited = []
    while node:
        visited.append(node["value"])
        steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                      "current": node["value"], "visited": list(visited),
                      "description": f"At node {node['value']}"})

        if a < node["value"] and b < node["value"]:
            steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                          "current": node["value"], "visited": list(visited),
                          "description": f"Both {a},{b} < {node['value']} → go left"})
            node = node.get("left")
        elif a > node["value"] and b > node["value"]:
            steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                          "current": node["value"], "visited": list(visited),
                          "description": f"Both {a},{b} > {node['value']} → go right"})
            node = node.get("right")
        else:
            steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                          "current": node["value"], "visited": list(visited),
                          "highlighted": [node["value"]],
                          "description": f"LCA of {a} and {b} = {node['value']}"})
            return steps

    steps.append({"step": len(steps) + 1, "description": "LCA not found"})
    return steps


def tree_height(values: list[int]) -> list[dict]:
    root = _build_bst(values)
    steps = []
    steps.append({"step": 1, "tree": _to_dict(root), "description": "Computing tree height"})

    def height(node, depth):
        if not node:
            return 0
        steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                      "current": node["value"],
                      "description": f"Visit {node['value']} at depth {depth}"})
        lh = height(node.get("left"), depth + 1)
        rh = height(node.get("right"), depth + 1)
        h = 1 + max(lh, rh)
        steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                      "current": node["value"],
                      "description": f"Height at {node['value']} = 1 + max({lh},{rh}) = {h}"})
        return h

    h = height(root, 0)
    steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                  "description": f"Tree height = {h}"})
    return steps


def tree_diameter(values: list[int]) -> list[dict]:
    root = _build_bst(values)
    steps = []
    max_diam = [0]

    steps.append({"step": 1, "tree": _to_dict(root), "description": "Computing tree diameter"})

    def height(node):
        if not node:
            return 0
        lh = height(node.get("left"))
        rh = height(node.get("right"))
        diam = lh + rh
        if diam > max_diam[0]:
            max_diam[0] = diam
            steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                          "current": node["value"],
                          "description": f"New max diameter at {node['value']}: {lh} + {rh} = {diam}"})
        return 1 + max(lh, rh)

    height(root)
    steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                  "description": f"Tree diameter = {max_diam[0]}"})
    return steps
