"""Counting Sort — O(n+k) time, O(k) space, Stable"""


def counting_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []

    if not a:
        return steps

    max_val = max(a)
    count = [0] * (max_val + 1)

    # Counting phase
    for i in range(n):
        count[a[i]] += 1
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "current": i,
            "active": [i],
            "description": f"Count: element {a[i]} → count[{a[i]}] = {count[a[i]]}",
        })

    # Placement phase
    idx = 0
    sorted_so_far = []
    for val in range(max_val + 1):
        for _ in range(count[val]):
            old_val = a[idx]
            a[idx] = val
            sorted_so_far.append(idx)

            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "swap": [idx] if old_val != val else [],
                "active": [idx],
                "sorted": list(sorted_so_far),
                "description": f"Place {val} at index {idx}",
            })
            idx += 1

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
