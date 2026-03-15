"""Jump Search — O(√n) time, O(1) space"""
import math


def jump_search(arr: list[int], target: int) -> list[dict]:
    a = sorted(arr)
    n = len(a)
    steps = []
    block = int(math.sqrt(n))
    prev = 0
    curr = block

    # Jump phase
    while curr < n and a[min(curr, n) - 1] < target:
        steps.append({
            "step": len(steps) + 1,
            "array": a,
            "current": min(curr, n) - 1,
            "range": [prev, min(curr, n) - 1],
            "pointers": {"block_start": prev, "block_end": min(curr, n) - 1},
            "description": f"Jump: a[{min(curr,n)-1}]={a[min(curr,n)-1]} < {target}, skip block [{prev}..{min(curr,n)-1}]",
        })
        prev = curr
        curr += block
        if prev >= n:
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "description": f"{target} not found (jumped past end)",
            })
            return steps

    # Linear scan phase
    scan_end = min(curr, n)
    steps.append({
        "step": len(steps) + 1,
        "array": a,
        "range": [prev, scan_end - 1],
        "description": f"Linear scan in block [{prev}..{scan_end - 1}]",
    })

    for i in range(prev, scan_end):
        if a[i] == target:
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "current": i,
                "found": [i],
                "range": [prev, scan_end - 1],
                "description": f"Found {target} at index {i}!",
            })
            return steps
        elif a[i] > target:
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "current": i,
                "range": [prev, scan_end - 1],
                "description": f"a[{i}]={a[i]} > {target}, stop",
            })
            break
        else:
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "current": i,
                "range": [prev, scan_end - 1],
                "description": f"a[{i}]={a[i]} ≠ {target}",
            })

    steps.append({
        "step": len(steps) + 1,
        "array": a,
        "description": f"{target} not found",
    })
    return steps
