"""Bubble Sort — O(n²) time, O(1) space, Stable"""


def bubble_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    sorted_indices = []

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "compare": [j, j + 1],
                "sorted": list(sorted_indices),
                "description": f"Compare {a[j]} and {a[j+1]}",
            })
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swapped = True
                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "swap": [j, j + 1],
                    "sorted": list(sorted_indices),
                    "description": f"Swap {a[j+1]} and {a[j]}",
                })
        sorted_indices.append(n - 1 - i)
        if not swapped:
            break

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
