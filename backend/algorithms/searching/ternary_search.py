"""Ternary Search — O(log₃n) time, O(1) space"""


def ternary_search(arr: list[int], target: int) -> list[dict]:
    a = sorted(arr)
    n = len(a)
    steps = []
    lo, hi = 0, n - 1

    while lo <= hi:
        mid1 = lo + (hi - lo) // 3
        mid2 = hi - (hi - lo) // 3

        steps.append({
            "step": len(steps) + 1, "array": a,
            "compare": [mid1, mid2],
            "range": [lo, hi],
            "pointers": {"low": lo, "mid1": mid1, "mid2": mid2, "high": hi},
            "description": f"Thirds: mid1={mid1} ({a[mid1]}), mid2={mid2} ({a[mid2]})",
        })

        if a[mid1] == target:
            steps.append({"step": len(steps) + 1, "array": a,
                          "found": [mid1],
                          "description": f"Found {target} at mid1={mid1}!"})
            return steps
        if a[mid2] == target:
            steps.append({"step": len(steps) + 1, "array": a,
                          "found": [mid2],
                          "description": f"Found {target} at mid2={mid2}!"})
            return steps

        if target < a[mid1]:
            hi = mid1 - 1
            steps.append({"step": len(steps) + 1, "array": a,
                          "range": [lo, hi],
                          "pointers": {"low": lo, "high": hi},
                          "description": f"{target} < {a[mid1]} → search left [{lo}..{hi}]"})
        elif target > a[mid2]:
            lo = mid2 + 1
            steps.append({"step": len(steps) + 1, "array": a,
                          "range": [lo, hi],
                          "pointers": {"low": lo, "high": hi},
                          "description": f"{target} > {a[mid2]} → search right [{lo}..{hi}]"})
        else:
            lo = mid1 + 1
            hi = mid2 - 1
            steps.append({"step": len(steps) + 1, "array": a,
                          "range": [lo, hi],
                          "pointers": {"low": lo, "high": hi},
                          "description": f"{a[mid1]} < {target} < {a[mid2]} → search middle [{lo}..{hi}]"})

    steps.append({"step": len(steps) + 1, "array": a,
                  "description": f"{target} not found"})
    return steps
