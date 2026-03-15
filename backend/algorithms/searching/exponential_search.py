"""Exponential Search — O(log n) time, O(1) space"""


def exponential_search(arr: list[int], target: int) -> list[dict]:
    a = sorted(arr)
    n = len(a)
    steps = []

    if a[0] == target:
        steps.append({"step": 1, "array": a, "found": [0],
                      "description": f"Found {target} at index 0!"})
        return steps

    # Exponential expansion
    bound = 1
    while bound < n and a[bound] <= target:
        steps.append({
            "step": len(steps) + 1, "array": a,
            "current": bound, "active": [bound],
            "description": f"Expand: bound={bound}, a[{bound}]={a[bound]} {'<=' if a[bound] <= target else '>'} {target}",
        })
        bound *= 2

    # Binary search in [bound/2, min(bound, n-1)]
    lo = bound // 2
    hi = min(bound, n - 1)
    steps.append({
        "step": len(steps) + 1, "array": a,
        "range": [lo, hi],
        "pointers": {"low": lo, "high": hi},
        "description": f"Binary search in [{lo}..{hi}]",
    })

    while lo <= hi:
        mid = (lo + hi) // 2
        steps.append({
            "step": len(steps) + 1, "array": a,
            "current": mid, "range": [lo, hi],
            "pointers": {"low": lo, "mid": mid, "high": hi},
            "description": f"mid={mid}, a[{mid}]={a[mid]}",
        })

        if a[mid] == target:
            steps.append({"step": len(steps) + 1, "array": a, "found": [mid],
                          "pointers": {"low": lo, "mid": mid, "high": hi},
                          "description": f"Found {target} at index {mid}!"})
            return steps
        elif a[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1

    steps.append({"step": len(steps) + 1, "array": a,
                  "description": f"{target} not found"})
    return steps
