"""Linear Search — O(n) time, O(1) space"""


def linear_search(arr: list[int], target: int) -> list[dict]:
    a = list(arr)
    steps = []
    checked = []

    for i in range(len(a)):
        checked.append(i)
        if a[i] == target:
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "current": i,
                "found": [i],
                "sorted": list(checked),
                "description": f"Index {i}: {a[i]} == {target} → Found!",
            })
            return steps
        else:
            steps.append({
                "step": len(steps) + 1,
                "array": a,
                "current": i,
                "sorted": checked[:-1],
                "description": f"Index {i}: {a[i]} ≠ {target}",
            })

    steps.append({
        "step": len(steps) + 1,
        "array": a,
        "sorted": list(checked),
        "description": f"{target} not found in array",
    })
    return steps
