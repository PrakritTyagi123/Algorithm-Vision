"""Bitonic Sort — O(n log²n) time, O(1) space, Unstable (parallel-friendly)"""


def bitonic_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []

    # Record initial state
    steps.append({
        "step": 1,
        "array": list(a),
        "description": f"Bitonic sort: {n} elements",
    })

    # Pad to power of 2
    size = 1
    max_val = max(a) + 1
    while size < n:
        size *= 2
    a.extend([max_val] * (size - n))

    _bitonic_sort(a, 0, size, True, steps, n)

    a = a[:n]
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps


def _bitonic_sort(a, lo, cnt, ascending, steps, n):
    if cnt <= 1:
        return
    k = cnt // 2
    _bitonic_sort(a, lo, k, True, steps, n)
    _bitonic_sort(a, lo + k, k, False, steps, n)
    _bitonic_merge(a, lo, cnt, ascending, steps, n)


def _bitonic_merge(a, lo, cnt, ascending, steps, n):
    if cnt <= 1:
        return
    k = cnt // 2
    for i in range(lo, lo + k):
        # Only show steps involving original array indices
        if i >= n and i + k >= n:
            if (a[i] > a[i + k]) == ascending:
                a[i], a[i + k] = a[i + k], a[i]
            continue

        if (a[i] > a[i + k]) == ascending:
            steps.append({
                "step": len(steps) + 1,
                "array": a[:n],
                "compare": [i, i + k] if i < n and i + k < n else [i] if i < n else [],
                "description": f"Compare index {i} ({a[i]}) and {i+k} ({a[i+k]})",
            })
            a[i], a[i + k] = a[i + k], a[i]
            steps.append({
                "step": len(steps) + 1,
                "array": a[:n],
                "swap": [i, i + k] if i < n and i + k < n else [i] if i < n else [],
                "description": f"Swap → [{a[i]}, {a[i+k]}]",
            })

    _bitonic_merge(a, lo, k, ascending, steps, n)
    _bitonic_merge(a, lo + k, k, ascending, steps, n)
