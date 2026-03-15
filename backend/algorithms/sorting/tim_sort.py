"""Tim Sort (simplified) — O(n log n) time, O(n) space, Stable"""

MIN_RUN = 32


def tim_sort(arr: list[int]) -> list[dict]:
    a = list(arr)
    n = len(a)
    steps = []
    min_run = min(MIN_RUN, n)

    # Phase 1: Insertion sort on small runs
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "active": list(range(start, end + 1)),
            "description": f"Run [{start}..{end}]: insertion sort",
        })
        for i in range(start + 1, end + 1):
            key = a[i]
            j = i - 1
            while j >= start and a[j] > key:
                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "compare": [j, j + 1],
                    "range": [start, end],
                    "description": f"Compare {a[j]} > {key}",
                })
                a[j + 1] = a[j]
                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "swap": [j, j + 1],
                    "range": [start, end],
                    "description": f"Shift {a[j]} right",
                })
                j -= 1
            a[j + 1] = key

        steps.append({
            "step": len(steps) + 1,
            "array": list(a),
            "sorted": list(range(start, end + 1)),
            "description": f"Run [{start}..{end}] sorted: {a[start:end+1]}",
        })

    # Phase 2: Merge runs
    size = min_run
    while size < n:
        for lo in range(0, n, size * 2):
            mid = min(lo + size - 1, n - 1)
            hi = min(lo + 2 * size - 1, n - 1)
            if mid < hi:
                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "active": list(range(lo, hi + 1)),
                    "description": f"Merge [{lo}..{mid}] + [{mid+1}..{hi}]",
                })

                left = a[lo:mid + 1]
                right = a[mid + 1:hi + 1]
                i = j = 0
                k = lo

                while i < len(left) and j < len(right):
                    steps.append({
                        "step": len(steps) + 1,
                        "array": list(a),
                        "compare": [lo + i, mid + 1 + j] if lo + i < n and mid + 1 + j < n else [],
                        "range": [lo, hi],
                        "description": f"Merge compare: {left[i]} vs {right[j]}",
                    })
                    if left[i] <= right[j]:
                        a[k] = left[i]
                        i += 1
                    else:
                        a[k] = right[j]
                        j += 1
                    k += 1

                while i < len(left):
                    a[k] = left[i]
                    i += 1
                    k += 1
                while j < len(right):
                    a[k] = right[j]
                    j += 1
                    k += 1

                steps.append({
                    "step": len(steps) + 1,
                    "array": list(a),
                    "sorted": list(range(lo, hi + 1)),
                    "description": f"Merged [{lo}..{hi}]: {a[lo:hi+1]}",
                })
        size *= 2

    steps.append({
        "step": len(steps) + 1,
        "array": list(a),
        "sorted": list(range(n)),
        "description": "Array is sorted!",
    })
    return steps
