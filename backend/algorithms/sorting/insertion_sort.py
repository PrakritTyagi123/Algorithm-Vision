"""Insertion Sort — O(n²) time, O(1) space, Stable"""


def insertion_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []

    for i in range(1, n):
        key = a[i]
        j = i - 1
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "active": [i],
            "sorted": list(range(i)),
            "description": f"Pick element {key} at index {i}",
        })

        while j >= 0 and a[j] > key:
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "compare": [j, j + 1],
                "sorted": list(range(i)),
                "description": f"Compare: {a[j]} > {key}",
            })
            a[j + 1] = a[j]
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "swap": [j, j + 1],
                "sorted": list(range(i)),
                "description": f"Shift {a[j]} right to index {j + 1}",
            })
            j -= 1

        a[j + 1] = key
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "active": [j + 1],
            "sorted": list(range(i + 1)),
            "description": f"Place {key} at index {j + 1}",
        })

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
