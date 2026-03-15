"""Heap Sort — O(n log n) time, O(1) space, Unstable"""


def heap_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    sorted_indices = []

    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify(a, n, i, steps, sorted_indices)

    # Extract elements
    for i in range(n - 1, 0, -1):
        a[0], a[i] = a[i], a[0]
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "swap": [0, i],
            "sorted": list(sorted_indices),
            "description": f"Swap root {a[i]} with index {i}",
        })
        sorted_indices.append(i)
        _heapify(a, i, 0, steps, sorted_indices)

    sorted_indices.append(0)
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps


def _heapify(a: list[int], n: int, i: int, steps: list[dict], sorted_indices: list[int]):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n:
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "compare": [largest, left],
            "sorted": list(sorted_indices),
            "description": f"Heapify: compare {a[largest]} with left child {a[left]}",
        })
        if a[left] > a[largest]:
            largest = left

    if right < n:
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "compare": [largest, right],
            "sorted": list(sorted_indices),
            "description": f"Heapify: compare {a[largest]} with right child {a[right]}",
        })
        if a[right] > a[largest]:
            largest = right

    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "swap": [i, largest],
            "sorted": list(sorted_indices),
            "description": f"Heapify swap index {i} and {largest}",
        })
        _heapify(a, n, largest, steps, sorted_indices)
