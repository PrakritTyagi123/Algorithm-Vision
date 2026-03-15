"""Data Structure Operations with step-by-step visualization."""


def heap_operations(values: list[int]) -> list[dict]:
    steps = []
    heap = []

    def _sift_up(i):
        while i > 0:
            parent = (i - 1) // 2
            if heap[i] < heap[parent]:
                steps.append({"step": len(steps) + 1, "array": list(heap),
                              "compare": [i, parent],
                              "description": f"Sift up: {heap[i]} < {heap[parent]}"})
                heap[i], heap[parent] = heap[parent], heap[i]
                steps.append({"step": len(steps) + 1, "array": list(heap),
                              "swap": [i, parent], "description": "Swap"})
                i = parent
            else:
                break

    def _sift_down(i, size):
        while 2 * i + 1 < size:
            child = 2 * i + 1
            if child + 1 < size and heap[child + 1] < heap[child]:
                child += 1
            if heap[child] < heap[i]:
                steps.append({"step": len(steps) + 1, "array": list(heap),
                              "compare": [i, child],
                              "description": f"Sift down: swap {heap[i]} with {heap[child]}"})
                heap[i], heap[child] = heap[child], heap[i]
                i = child
            else:
                break

    # Insert all values
    for v in values:
        heap.append(v)
        steps.append({"step": len(steps) + 1, "array": list(heap),
                      "active": [len(heap) - 1],
                      "description": f"Insert {v}"})
        _sift_up(len(heap) - 1)

    steps.append({"step": len(steps) + 1, "array": list(heap),
                  "description": f"Min-heap built: {list(heap)}"})

    # Extract min 3 times
    for _ in range(min(3, len(heap))):
        if not heap:
            break
        min_val = heap[0]
        heap[0] = heap[-1]
        heap.pop()
        steps.append({"step": len(steps) + 1, "array": list(heap),
                      "description": f"Extract min: {min_val}"})
        if heap:
            _sift_down(0, len(heap))

    return steps


def linked_list_operations(values: list[int]) -> list[dict]:
    steps = []
    ll = list(values)

    # Build
    steps.append({"step": len(steps) + 1, "array": list(ll),
                  "description": f"Linked list: {ll}"})

    # Insert at head
    ll.insert(0, 99)
    steps.append({"step": len(steps) + 1, "array": list(ll), "active": [0],
                  "description": "Insert 99 at head"})

    # Insert at tail
    ll.append(77)
    steps.append({"step": len(steps) + 1, "array": list(ll), "active": [len(ll) - 1],
                  "description": "Insert 77 at tail"})

    # Delete from middle
    if len(ll) > 3:
        mid = len(ll) // 2
        removed = ll.pop(mid)
        steps.append({"step": len(steps) + 1, "array": list(ll),
                      "description": f"Delete index {mid} (value {removed})"})

    # Reverse
    steps.append({"step": len(steps) + 1, "array": list(ll),
                  "description": "Reversing linked list..."})

    for i in range(len(ll) // 2):
        j = len(ll) - 1 - i
        ll[i], ll[j] = ll[j], ll[i]
        steps.append({"step": len(steps) + 1, "array": list(ll),
                      "swap": [i, j],
                      "description": f"Swap index {i} ↔ {j}"})

    steps.append({"step": len(steps) + 1, "array": list(ll),
                  "sorted": list(range(len(ll))),
                  "description": f"Reversed: {ll}"})

    # Floyd's cycle detection demo (on non-cyclic list)
    slow = fast = 0
    steps.append({"step": len(steps) + 1, "array": list(ll),
                  "description": "Floyd's cycle detection: slow and fast pointers"})
    while fast < len(ll) and fast + 1 < len(ll):
        slow += 1
        fast += 2
        steps.append({"step": len(steps) + 1, "array": list(ll),
                      "pointers": {"slow": min(slow, len(ll) - 1), "fast": min(fast, len(ll) - 1)},
                      "description": f"slow={slow}, fast={fast}"})

    steps.append({"step": len(steps) + 1, "array": list(ll),
                  "description": "No cycle detected"})
    return steps


def hash_table_operations(keys: list[int], table_size: int = 10) -> list[dict]:
    steps = []

    # ── Separate Chaining ──
    chains = [[] for _ in range(table_size)]
    steps.append({"step": len(steps) + 1,
                  "description": f"Hash table (chaining) with {table_size} buckets"})

    for key in keys:
        idx = key % table_size
        chains[idx].append(key)
        flat = []
        for i, chain in enumerate(chains):
            for v in chain:
                flat.append(v)
        steps.append({"step": len(steps) + 1,
                      "active": [idx],
                      "description": f"Insert {key}: hash={key}%{table_size}={idx}, bucket {idx}={chains[idx]}"})

    # Search
    search_key = keys[0] if keys else 5
    idx = search_key % table_size
    found = search_key in chains[idx]
    steps.append({"step": len(steps) + 1,
                  "active": [idx],
                  "description": f"Search {search_key}: bucket {idx}, {'found' if found else 'not found'}"})

    # ── Open Addressing (Linear Probing) ──
    table = [None] * table_size
    steps.append({"step": len(steps) + 1,
                  "description": f"\n--- Open Addressing (Linear Probing) ---"})

    for key in keys:
        idx = key % table_size
        probes = 0
        while table[idx] is not None:
            probes += 1
            steps.append({"step": len(steps) + 1,
                          "active": [idx],
                          "description": f"Insert {key}: collision at {idx} (occupied by {table[idx]})"})
            idx = (idx + 1) % table_size
        table[idx] = key
        display = [v if v is not None else 0 for v in table]
        steps.append({"step": len(steps) + 1,
                      "array": display, "active": [idx],
                      "description": f"Insert {key} at index {idx} ({probes} collisions)"})

    steps.append({"step": len(steps) + 1,
                  "array": [v if v is not None else 0 for v in table],
                  "description": f"Final hash table: {table}"})
    return steps


def stack_operations(values: list[int]) -> list[dict]:
    """Stack (LIFO): push all, then pop 3."""
    steps = []
    stack = []

    for v in values:
        stack.append(v)
        steps.append({
            "step": len(steps) + 1,
            "array": list(stack),
            "active": [len(stack) - 1],
            "pointers": {"top": len(stack) - 1},
            "description": f"Push {v} → top={len(stack)-1}",
        })

    steps.append({"step": len(steps) + 1, "array": list(stack),
                  "pointers": {"top": len(stack) - 1},
                  "description": f"Stack built: {list(stack)} (LIFO)"})

    for _ in range(min(3, len(stack))):
        val = stack.pop()
        steps.append({
            "step": len(steps) + 1,
            "array": list(stack),
            "swap": [len(stack)] if len(stack) < len(values) else [],
            "pointers": {"top": len(stack) - 1} if stack else {},
            "description": f"Pop → {val}",
        })

    steps.append({"step": len(steps) + 1, "array": list(stack),
                  "description": f"Stack after 3 pops: {list(stack)}"})
    return steps


def queue_operations(values: list[int]) -> list[dict]:
    """Queue (FIFO): enqueue all, then dequeue 3."""
    steps = []
    queue = []

    for v in values:
        queue.append(v)
        steps.append({
            "step": len(steps) + 1,
            "array": list(queue),
            "active": [len(queue) - 1],
            "pointers": {"front": 0, "rear": len(queue) - 1},
            "description": f"Enqueue {v} → rear={len(queue)-1}",
        })

    steps.append({"step": len(steps) + 1, "array": list(queue),
                  "pointers": {"front": 0, "rear": len(queue) - 1},
                  "description": f"Queue built: {list(queue)} (FIFO)"})

    for _ in range(min(3, len(queue))):
        val = queue.pop(0)
        steps.append({
            "step": len(steps) + 1,
            "array": list(queue),
            "swap": [0] if queue else [],
            "pointers": {"front": 0, "rear": len(queue) - 1} if queue else {},
            "description": f"Dequeue → {val}",
        })

    steps.append({"step": len(steps) + 1, "array": list(queue),
                  "description": f"Queue after 3 dequeues: {list(queue)}"})
    return steps
