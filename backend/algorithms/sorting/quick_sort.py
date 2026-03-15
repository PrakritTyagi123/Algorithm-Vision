"""Quick Sort — O(n log n) avg time, O(log n) space, Unstable"""


def quick_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    steps = []
    _quick_sort_recurse(a, 0, len(a) - 1, steps)
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(len(a))),
        "description": "Array is sorted!",
    })
    return steps


def _quick_sort_recurse(a: list[int], lo: int, hi: int, steps: list[dict]):
    if lo >= hi:
        return

    pivot_val = a[hi]
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "active": [hi],
        "range": [lo, hi],
        "pointers": {"pivot": hi},
        "description": f"Pivot = {pivot_val} (index {hi})",
    })

    i = lo
    for j in range(lo, hi):
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "compare": [j, hi],
            "pointers": {"i": i, "j": j, "pivot": hi},
            "range": [lo, hi],
            "description": f"Compare {a[j]} with pivot {pivot_val}",
        })
        if a[j] <= pivot_val:
            if i != j:
                a[i], a[j] = a[j], a[i]
                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "swap": [i, j],
                    "range": [lo, hi],
                    "description": f"Swap index {i} and {j}",
                })
            i += 1

    a[i], a[hi] = a[hi], a[i]
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "swap": [i, hi],
        "description": f"Place pivot {pivot_val} at index {i}",
    })

    _quick_sort_recurse(a, lo, i - 1, steps)
    _quick_sort_recurse(a, i + 1, hi, steps)
