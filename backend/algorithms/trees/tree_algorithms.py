"""Tree Algorithms with step-by-step visualization."""


def _to_dict(node):
    """Convert tree node to serializable dict."""
    if node is None:
        return None
    d = {"value": node["value"], "left": _to_dict(node.get("left")), "right": _to_dict(node.get("right"))}
    if "bf" in node:
        d["bf"] = node["bf"]
    if "color" in node:
        d["color"] = node["color"]
    return d


def build_bst(values: list[int]) -> dict:
    root = None
    for v in values:
        root = _bst_insert(root, v)
    return root


def _bst_insert(node, val):
    if node is None:
        return {"value": val, "left": None, "right": None}
    if val < node["value"]:
        node["left"] = _bst_insert(node["left"], val)
    elif val > node["value"]:
        node["right"] = _bst_insert(node["right"], val)
    return node


def bst_operations(values: list[int]) -> list[dict]:
    steps = []
    root = None
    for v in values:
        root = _bst_insert(root, v)
        steps.append({"step": len(steps)+1, "tree": _to_dict(root),
                      "inserted": v, "description": f"Insert {v}"})
    return steps


def inorder_traversal(values: list[int]) -> list[dict]:
    root = build_bst(values)
    steps = []
    visited = []

    def inorder(node):
        if not node:
            return
        inorder(node.get("left"))
        visited.append(node["value"])
        steps.append({"step": len(steps)+1, "tree": _to_dict(root),
                      "current": node["value"], "visited": list(visited),
                      "description": f"Visit {node['value']}"})
        inorder(node.get("right"))

    steps.append({"step": 1, "tree": _to_dict(root), "description": "Inorder: Left → Root → Right"})
    inorder(root)
    return steps


def preorder_traversal(values: list[int]) -> list[dict]:
    root = build_bst(values)
    steps = []
    visited = []

    def preorder(node):
        if not node:
            return
        visited.append(node["value"])
        steps.append({"step": len(steps)+1, "tree": _to_dict(root),
                      "current": node["value"], "visited": list(visited),
                      "description": f"Visit {node['value']}"})
        preorder(node.get("left"))
        preorder(node.get("right"))

    steps.append({"step": 1, "tree": _to_dict(root), "description": "Preorder: Root → Left → Right"})
    preorder(root)
    return steps


def postorder_traversal(values: list[int]) -> list[dict]:
    root = build_bst(values)
    steps = []
    visited = []

    def postorder(node):
        if not node:
            return
        postorder(node.get("left"))
        postorder(node.get("right"))
        visited.append(node["value"])
        steps.append({"step": len(steps)+1, "tree": _to_dict(root),
                      "current": node["value"], "visited": list(visited),
                      "description": f"Visit {node['value']}"})

    steps.append({"step": 1, "tree": _to_dict(root), "description": "Postorder: Left → Right → Root"})
    postorder(root)
    return steps


def levelorder_traversal(values: list[int]) -> list[dict]:
    root = build_bst(values)
    steps = []
    visited = []

    if not root:
        return steps

    steps.append({"step": 1, "tree": _to_dict(root), "description": "Level-order (BFS)"})
    queue = [root]
    while queue:
        node = queue.pop(0)
        visited.append(node["value"])
        steps.append({"step": len(steps)+1, "tree": _to_dict(root),
                      "current": node["value"], "visited": list(visited),
                      "description": f"Visit {node['value']}"})
        if node.get("left"):
            queue.append(node["left"])
        if node.get("right"):
            queue.append(node["right"])

    return steps


def avl_operations(values: list[int]) -> list[dict]:
    steps = []
    root = None

    def height(node):
        if not node:
            return 0
        return node.get("h", 0)

    def update_height(node):
        node["h"] = 1 + max(height(node.get("left")), height(node.get("right")))
        node["bf"] = height(node.get("left")) - height(node.get("right"))

    def rotate_right(y):
        x = y["left"]
        t = x.get("right")
        x["right"] = y
        y["left"] = t
        update_height(y)
        update_height(x)
        return x

    def rotate_left(x):
        y = x["right"]
        t = y.get("left")
        y["left"] = x
        x["right"] = t
        update_height(x)
        update_height(y)
        return y

    def insert(node, val):
        if not node:
            return {"value": val, "left": None, "right": None, "h": 1, "bf": 0}
        if val < node["value"]:
            node["left"] = insert(node["left"], val)
        elif val > node["value"]:
            node["right"] = insert(node["right"], val)
        else:
            return node

        update_height(node)
        bf = node["bf"]

        if bf > 1 and val < node["left"]["value"]:
            steps.append({"step": len(steps)+1, "tree": _to_dict(node),
                          "rotated": [node["value"]], "description": f"Right rotate at {node['value']}"})
            return rotate_right(node)
        if bf < -1 and val > node["right"]["value"]:
            steps.append({"step": len(steps)+1, "tree": _to_dict(node),
                          "rotated": [node["value"]], "description": f"Left rotate at {node['value']}"})
            return rotate_left(node)
        if bf > 1 and val > node["left"]["value"]:
            node["left"] = rotate_left(node["left"])
            steps.append({"step": len(steps)+1, "tree": _to_dict(node),
                          "rotated": [node["value"]], "description": f"Left-Right rotate at {node['value']}"})
            return rotate_right(node)
        if bf < -1 and val < node["right"]["value"]:
            node["right"] = rotate_right(node["right"])
            steps.append({"step": len(steps)+1, "tree": _to_dict(node),
                          "rotated": [node["value"]], "description": f"Right-Left rotate at {node['value']}"})
            return rotate_left(node)

        return node

    for v in values:
        root = insert(root, v)
        steps.append({"step": len(steps)+1, "tree": _to_dict(root),
                      "inserted": v, "description": f"Insert {v}"})

    return steps
