"""Shell Sort — O(n log²n) time, O(1) space, Unstable"""


def shell_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    gap = n // 2

    while gap > 0:
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "description": f"Gap = {gap}",
        })
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "compare": [j - gap, j],
                    "description": f"Compare index {j-gap} ({a[j-gap]}) > {temp}",
                })
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
            if j != i:
                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "swap": [j, i],
                    "description": f"Place {temp} at index {j}",
                })
        gap //= 2

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
