"""Binary Search — O(log n) time, O(1) space"""


def binary_search(arr: list[int], target: int) -> list[dict]:
    a = sorted(arr)
    steps = []
    lo, hi = 0, len(a) - 1
    eliminated = []

    while lo <= hi:
        mid = (lo + hi) // 2

        steps.append({
            "step": len(steps) + 1,
            "array": a,
            "current": mid,
            "range": [lo, hi],
            "pointers": {"low": lo, "mid": mid, "high": hi},
            "description": f"mid={mid}, a[{mid}]={a[mid]}, target={target}",
        })

        if a[mid] == target:
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "found": [mid],
                "range": [lo, hi],
                "pointers": {"low": lo, "mid": mid, "high": hi},
                "description": f"Found {target} at index {mid}!",
            })
            return steps
        elif a[mid] < target:
            # Eliminate left half
            for i in range(lo, mid + 1):
                if i not in eliminated:
                    eliminated.append(i)
            lo = mid + 1
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "range": [lo, hi],
                "current": mid,
                "pointers": {"low": lo, "high": hi},
                "description": f"{a[mid]} < {target} → search right [{lo}..{hi}]",
            })
        else:
            # Eliminate right half
            for i in range(mid, hi + 1):
                if i not in eliminated:
                    eliminated.append(i)
            hi = mid - 1
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "range": [lo, hi] if lo <= hi else [lo, lo],
                "current": mid,
                "pointers": {"low": lo, "high": hi},
                "description": f"{a[mid]} > {target} → search left [{lo}..{hi}]",
            })

    steps.append({
        "step": len(steps) + 1,
        "array": a,
        "description": f"{target} not found in array",
    })
    return steps
