"""Red-Black Tree — O(log n) operations with color balancing."""


def red_black_tree(values: list[int]) -> list[dict]:
    steps = []
    root = None

    def _new_node(val, color="red"):
        return {"value": val, "left": None, "right": None, "color": color}

    def _to_dict(node):
        if not node:
            return None
        return {"value": node["value"], "left": _to_dict(node.get("left")),
                "right": _to_dict(node.get("right")), "color": node.get("color", "black")}

    def _rotate_left(node):
        x = node["right"]
        node["right"] = x.get("left")
        x["left"] = node
        x["color"] = node["color"]
        node["color"] = "red"
        return x

    def _rotate_right(node):
        x = node["left"]
        node["left"] = x.get("right")
        x["right"] = node
        x["color"] = node["color"]
        node["color"] = "red"
        return x

    def _flip_colors(node):
        node["color"] = "red"
        if node.get("left"):
            node["left"]["color"] = "black"
        if node.get("right"):
            node["right"]["color"] = "black"

    def _is_red(node):
        return node is not None and node.get("color") == "red"

    def _insert(node, val):
        if node is None:
            return _new_node(val)

        if val < node["value"]:
            node["left"] = _insert(node["left"], val)
        elif val > node["value"]:
            node["right"] = _insert(node["right"], val)

        # Fix-up
        if _is_red(node.get("right")) and not _is_red(node.get("left")):
            node = _rotate_left(node)
            steps.append({"step": len(steps) + 1, "tree": _to_dict(root_ref[0]),
                          "rotated": [node["value"]], "description": f"Left rotate at {node['value']}"})

        if _is_red(node.get("left")) and _is_red(node.get("left", {}).get("left")):
            node = _rotate_right(node)
            steps.append({"step": len(steps) + 1, "tree": _to_dict(root_ref[0]),
                          "rotated": [node["value"]], "description": f"Right rotate at {node['value']}"})

        if _is_red(node.get("left")) and _is_red(node.get("right")):
            _flip_colors(node)
            steps.append({"step": len(steps) + 1, "tree": _to_dict(root_ref[0]),
                          "description": f"Flip colors at {node['value']}"})

        return node

    root_ref = [None]
    for v in values:
        root_ref[0] = _insert(root_ref[0], v)
        if root_ref[0]:
            root_ref[0]["color"] = "black"
        root = root_ref[0]
        steps.append({"step": len(steps) + 1, "tree": _to_dict(root),
                      "inserted": v, "description": f"Insert {v}"})

    return steps


"""Segment Tree — O(n) build, O(log n) query/update."""


def segment_tree(values: list[int]) -> list[dict]:
    steps = []
    n = len(values)
    tree = [0] * (4 * n)

    def build(node, start, end):
        if start == end:
            tree[node] = values[start]
            steps.append({"step": len(steps) + 1,
                          "array": values, "active": [start],
                          "description": f"Leaf node[{node}] = values[{start}] = {values[start]}"})
            return
        mid = (start + end) // 2
        build(2 * node, start, mid)
        build(2 * node + 1, mid + 1, end)
        tree[node] = tree[2 * node] + tree[2 * node + 1]
        steps.append({"step": len(steps) + 1,
                      "array": values, "active": list(range(start, end + 1)),
                      "description": f"node[{node}] = sum[{start}..{end}] = {tree[node]}"})

    build(1, 0, n - 1)

    # Demo a range query
    def query(node, start, end, l, r):
        if r < start or end < l:
            return 0
        if l <= start and end <= r:
            steps.append({"step": len(steps) + 1,
                          "array": values, "active": list(range(start, end + 1)),
                          "found": list(range(start, end + 1)),
                          "description": f"Query [{l}..{r}]: node[{node}] covers [{start}..{end}] = {tree[node]}"})
            return tree[node]
        mid = (start + end) // 2
        steps.append({"step": len(steps) + 1,
                      "array": values, "active": list(range(start, end + 1)),
                      "description": f"Query [{l}..{r}]: split at node[{node}] [{start}..{end}]"})
        return query(2 * node, start, mid, l, r) + query(2 * node + 1, mid + 1, end, l, r)

    if n > 2:
        result = query(1, 0, n - 1, 1, n - 2)
        steps.append({"step": len(steps) + 1, "array": values,
                      "description": f"Query sum[1..{n-2}] = {result}"})
    return steps


"""Fenwick Tree (BIT) — O(n) build, O(log n) query/update."""


def fenwick_tree(values: list[int]) -> list[dict]:
    steps = []
    n = len(values)
    bit = [0] * (n + 1)

    def update(i, delta):
        idx = i + 1
        while idx <= n:
            bit[idx] += delta
            steps.append({"step": len(steps) + 1,
                          "array": bit[1:],
                          "active": [idx - 1],
                          "description": f"BIT[{idx}] += {delta} → {bit[idx]}"})
            idx += idx & (-idx)

    def prefix_sum(i):
        s = 0
        idx = i + 1
        while idx > 0:
            s += bit[idx]
            steps.append({"step": len(steps) + 1,
                          "array": bit[1:],
                          "active": [idx - 1],
                          "description": f"Sum: add BIT[{idx}]={bit[idx]}, running={s}"})
            idx -= idx & (-idx)
        return s

    # Build
    for i, v in enumerate(values):
        update(i, v)

    steps.append({"step": len(steps) + 1, "array": bit[1:],
                  "description": f"Fenwick tree built from {values}"})

    # Demo prefix query
    if n > 2:
        result = prefix_sum(n - 1)
        steps.append({"step": len(steps) + 1, "array": bit[1:],
                      "description": f"Prefix sum [0..{n-1}] = {result}"})

    return steps


"""Trie — prefix tree for strings."""


def trie_operations(words: list[str] = None) -> list[dict]:
    if words is None:
        words = ["app", "ape", "bat", "bar", "cat"]

    steps = []
    trie = {}

    def _trie_to_tree(node, prefix=""):
        """Convert trie dict to binary tree dict for treeVisualizer."""
        if not node:
            return None
        children = []
        for char, child in sorted(node.items()):
            if char == "_end":
                continue
            child_tree = _trie_to_tree(child, prefix + char)
            if child_tree:
                children.append(child_tree)
        label = prefix[-1] if prefix else "⊙"
        # Use ordinal as value for treeVisualizer (needs numeric)
        val = ord(label) if len(label) == 1 and label != "⊙" else 0
        result = {"value": val, "left": None, "right": None}
        if len(children) >= 1:
            result["left"] = children[0]
        if len(children) >= 2:
            result["right"] = children[1]
        return result

    for word in words:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node["_end"] = True

        tree_dict = _trie_to_tree(trie)
        steps.append({
            "step": len(steps) + 1,
            "tree": tree_dict,
            "inserted": ord(word[-1]),
            "description": f"Insert '{word}'",
        })

    # Search demo
    search = words[0] if words else "app"
    node = trie
    for char in search:
        if char in node:
            node = node[char]
            steps.append({
                "step": len(steps) + 1,
                "tree": _trie_to_tree(trie),
                "current": ord(char),
                "description": f"Search '{search}': found '{char}'",
            })
    found = node.get("_end", False)
    steps.append({
        "step": len(steps) + 1,
        "tree": _trie_to_tree(trie),
        "description": f"Search '{search}': {'FOUND' if found else 'not found'}",
    })

    return steps

    return steps
