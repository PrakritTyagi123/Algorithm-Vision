"""Merge Sort — O(n log n) time, O(n) space, Stable"""


def merge_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    steps = []
    _merge_sort_recurse(a, 0, len(a) - 1, steps)
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(len(a))),
        "description": "Array is sorted!",
    })
    return steps


def _merge_sort_recurse(a: list[int], lo: int, hi: int, steps: list[dict]):
    if lo >= hi:
        return

    mid = (lo + hi) // 2
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "range": [lo, hi],
        "active": [mid],
        "description": f"Split [{lo}..{hi}] at mid={mid}",
    })

    _merge_sort_recurse(a, lo, mid, steps)
    _merge_sort_recurse(a, mid + 1, hi, steps)

    # Merge
    left = a[lo:mid + 1]
    right = a[mid + 1:hi + 1]
    i = j = 0
    k = lo

    while i < len(left) and j < len(right):
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "compare": [lo + i, mid + 1 + j],
            "range": [lo, hi],
            "description": f"Merge: compare {left[i]} and {right[j]}",
        })
        if left[i] <= right[j]:
            a[k] = left[i]
            i += 1
        else:
            a[k] = right[j]
            j += 1
        k += 1

    while i < len(left):
        a[k] = left[i]
        i += 1
        k += 1
    while j < len(right):
        a[k] = right[j]
        j += 1
        k += 1

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "range": [lo, hi],
        "sorted": list(range(lo, hi + 1)),
        "description": f"Merged [{lo}..{hi}]",
    })
