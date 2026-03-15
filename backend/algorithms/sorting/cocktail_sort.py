"""Cocktail Sort — O(n²) time, O(1) space, Stable (bidirectional bubble)"""


def cocktail_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    start = 0
    end = n - 1
    swapped = True

    while swapped:
        swapped = False
        for i in range(start, end):
            steps.append({"step": len(steps)+1, "array": list(a), "compare": [i, i+1],
                          "description": f"→ Compare {a[i]} and {a[i+1]}"})
            if a[i] > a[i + 1]:
                a[i], a[i+1] = a[i+1], a[i]
                swapped = True
                steps.append({"step": len(steps)+1, "array": list(a), "swap": [i, i+1],
                              "description": f"→ Swap"})
        end -= 1
        if not swapped:
            break
        swapped = False
        for i in range(end, start, -1):
            steps.append({"step": len(steps)+1, "array": list(a), "compare": [i-1, i],
                          "description": f"← Compare {a[i-1]} and {a[i]}"})
            if a[i - 1] > a[i]:
                a[i-1], a[i] = a[i], a[i-1]
                swapped = True
                steps.append({"step": len(steps)+1, "array": list(a), "swap": [i-1, i],
                              "description": f"← Swap"})
        start += 1

    steps.append({"step": len(steps)+1, "array": list(a), "sorted": list(range(n)),
                  "description": "Array is sorted!"})
    return steps
