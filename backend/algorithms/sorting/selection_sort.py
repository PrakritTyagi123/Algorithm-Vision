"""Selection Sort — O(n²) time, O(1) space, Unstable"""


def selection_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    sorted_indices = []

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "compare": [min_idx, j],
                "active": [i],
                "sorted": list(sorted_indices),
                "pointers": {"min": min_idx, "j": j},
                "description": f"Compare {a[min_idx]} (min) with {a[j]}",
            })
            if a[j] < a[min_idx]:
                min_idx = j

        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            steps.append({
                "step": len(steps) + 1,
                "array": list(a),
                "swap": [i, min_idx],
                "sorted": list(sorted_indices),
                "description": f"Swap index {i} and {min_idx}",
            })
        sorted_indices.append(i)

    sorted_indices.append(n - 1)
    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
