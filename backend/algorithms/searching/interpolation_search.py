"""Interpolation Search — O(log log n) avg time, O(1) space"""


def interpolation_search(arr: list[int], target: int) -> list[dict]:
    a = sorted(arr)
    n = len(a)
    steps = []
    lo, hi = 0, n - 1

    while lo <= hi and a[lo] <= target <= a[hi]:
        if lo == hi:
            if a[lo] == target:
                steps.append({"step": len(steps) + 1, "array": a, "found": [lo],
                              "pointers": {"pos": lo},
                              "description": f"Found {target} at index {lo}!"})
            else:
                steps.append({"step": len(steps) + 1, "array": a,
                              "description": f"{target} not found"})
            return steps

        denom = a[hi] - a[lo]
        pos = lo + ((target - a[lo]) * (hi - lo) // denom) if denom else lo
        pos = max(lo, min(pos, hi))

        steps.append({
            "step": len(steps) + 1, "array": a,
            "current": pos, "range": [lo, hi],
            "pointers": {"low": lo, "pos": pos, "high": hi},
            "description": f"Interpolate: pos={pos}, a[{pos}]={a[pos]}",
        })

        if a[pos] == target:
            steps.append({"step": len(steps) + 1, "array": a, "found": [pos],
                          "pointers": {"low": lo, "pos": pos, "high": hi},
                          "description": f"Found {target} at index {pos}!"})
            return steps
        elif a[pos] < target:
            lo = pos + 1
            steps.append({"step": len(steps) + 1, "array": a,
                          "range": [lo, hi], "current": pos,
                          "pointers": {"low": lo, "high": hi},
                          "description": f"{a[pos]} < {target} → search [{lo}..{hi}]"})
        else:
            hi = pos - 1
            steps.append({"step": len(steps) + 1, "array": a,
                          "range": [lo, hi], "current": pos,
                          "pointers": {"low": lo, "high": hi},
                          "description": f"{a[pos]} > {target} → search [{lo}..{hi}]"})

    steps.append({"step": len(steps) + 1, "array": a,
                  "description": f"{target} not found"})
    return steps
