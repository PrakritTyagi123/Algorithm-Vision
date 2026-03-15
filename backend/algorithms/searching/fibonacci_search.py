"""Fibonacci Search — O(log n) time, O(1) space"""


def fibonacci_search(arr: list[int], target: int) -> list[dict]:
    a = sorted(arr)
    n = len(a)
    steps = []

    # Find smallest fibonacci >= n
    fib2, fib1, fib = 0, 1, 1
    while fib < n:
        fib2, fib1, fib = fib1, fib, fib1 + fib

    offset = -1

    while fib > 1:
        i = min(offset + fib2, n - 1)

        steps.append({
            "step": len(steps) + 1, "array": a,
            "current": i,
            "pointers": {"probe": i},
            "description": f"Fibonacci probe: index {i}, a[{i}]={a[i]}",
        })

        if a[i] < target:
            fib, fib1, fib2 = fib1, fib2, fib1 - fib2
            offset = i
            steps.append({
                "step": len(steps) + 1, "array": a,
                "range": [offset + 1, min(offset + fib, n - 1)],
                "current": i,
                "description": f"{a[i]} < {target} → move right, offset={offset}",
            })
        elif a[i] > target:
            fib, fib1, fib2 = fib2, fib1 - fib2, fib - fib1
            steps.append({
                "step": len(steps) + 1, "array": a,
                "range": [offset + 1, i - 1] if offset + 1 <= i - 1 else [offset + 1, offset + 1],
                "current": i,
                "description": f"{a[i]} > {target} → move left",
            })
        else:
            steps.append({
                "step": len(steps) + 1, "array": a,
                "found": [i],
                "description": f"Found {target} at index {i}!",
            })
            return steps

    # Check last element
    if fib1 and offset + 1 < n and a[offset + 1] == target:
        steps.append({
            "step": len(steps) + 1, "array": a,
            "found": [offset + 1],
            "description": f"Found {target} at index {offset + 1}!",
        })
        return steps

    steps.append({"step": len(steps) + 1, "array": a,
                  "description": f"{target} not found"})
    return steps
