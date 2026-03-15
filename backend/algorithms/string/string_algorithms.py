"""String Algorithms with step-by-step visualization."""


def kmp_search(text: str, pattern: str) -> list[dict]:
    steps = []
    n, m = len(text), len(pattern)
    lps = _compute_lps(pattern)

    i = j = 0
    while i < n:
        steps.append({"step": len(steps)+1,
                      "table": [[ord(c) for c in text], [ord(c) for c in pattern] + [None]*(n-m)],
                      "row_headers": ["text", "pattern"],
                      "current": [0, i], "highlighted": [[1, j]] if j < m else [],
                      "description": f"Compare text[{i}]='{text[i]}' with pattern[{j}]='{pattern[j] if j<m else '?'}'"})
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == m:
                steps.append({"step": len(steps)+1,
                              "current": [0, i-m],
                              "description": f"Pattern found at index {i-m}!"})
                j = lps[j-1]
        else:
            if j != 0:
                j = lps[j-1]
            else:
                i += 1

    if not any("found" in s.get("description", "") for s in steps):
        steps.append({"step": len(steps)+1, "description": "Pattern not found"})
    return steps


def _compute_lps(pattern):
    m = len(pattern)
    lps = [0] * m
    length = 0
    i = 1
    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length-1]
        else:
            lps[i] = 0
            i += 1
    return lps


def rabin_karp(text: str, pattern: str) -> list[dict]:
    steps = []
    n, m = len(text), len(pattern)
    d, q = 256, 101
    h = pow(d, m-1, q)
    p_hash = t_hash = 0
    text_row = [ord(c) for c in text]

    for i in range(m):
        p_hash = (d * p_hash + ord(pattern[i])) % q
        t_hash = (d * t_hash + ord(text[i])) % q

    for i in range(n - m + 1):
        steps.append({"step": len(steps)+1,
                      "table": [text_row],
                      "col_headers": list(text),
                      "current": [0, i],
                      "highlighted": [[0, j] for j in range(i, min(i+m, n))],
                      "description": f"Window [{i}:{i+m}] hash={t_hash}, pattern_hash={p_hash}"})
        if p_hash == t_hash:
            match = text[i:i+m] == pattern
            if match:
                steps.append({"step": len(steps)+1,
                              "table": [text_row],
                              "col_headers": list(text),
                              "current": [0, i],
                              "found": list(range(i, i+m)),
                              "highlighted": [[0, j] for j in range(i, i+m)],
                              "description": f"Found pattern at index {i}!"})
            else:
                steps.append({"step": len(steps)+1,
                              "table": [text_row],
                              "col_headers": list(text),
                              "current": [0, i],
                              "description": f"Hash match but spurious hit"})
        if i < n - m:
            t_hash = (d * (t_hash - ord(text[i]) * h) + ord(text[i + m])) % q
            if t_hash < 0:
                t_hash += q

    if not any(s.get("found") for s in steps):
        steps.append({"step": len(steps)+1, "description": f"Pattern not found"})
    return steps


def boyer_moore(text: str, pattern: str) -> list[dict]:
    steps = []
    n, m = len(text), len(pattern)
    text_row = [ord(c) for c in text]

    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i

    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            steps.append({"step": len(steps)+1, "current": [0, s+j],
                          "table": [text_row],
                          "col_headers": list(text),
                          "highlighted": [[0, s+j]],
                          "description": f"Match: text[{s+j}]='{text[s+j]}' == pattern[{j}]"})
            j -= 1

        if j < 0:
            steps.append({"step": len(steps)+1, "current": [0, s],
                          "table": [text_row],
                          "col_headers": list(text),
                          "highlighted": [[0, i] for i in range(s, s+m)],
                          "found": list(range(s, s+m)),
                          "description": f"Found pattern at index {s}!"})
            s += (m - bad_char.get(text[s+m], -1)) if s+m < n else 1
        else:
            steps.append({"step": len(steps)+1, "current": [0, s+j],
                          "table": [text_row],
                          "col_headers": list(text),
                          "description": f"Mismatch: text[{s+j}]='{text[s+j]}' != pattern[{j}]='{pattern[j]}'"})
            shift = max(1, j - bad_char.get(text[s+j], -1))
            s += shift

    if not any(s.get("found") for s in steps):
        steps.append({"step": len(steps)+1, "description": "Pattern not found"})
    return steps


def z_algorithm(text: str, pattern: str) -> list[dict]:
    steps = []
    concat = pattern + "$" + text
    n = len(concat)
    z = [0] * n
    z[0] = n
    l = r = 0

    for i in range(1, n):
        if i < r:
            z[i] = min(r - i, z[i - l])
        while i + z[i] < n and concat[z[i]] == concat[i + z[i]]:
            z[i] += 1
        if i + z[i] > r:
            l, r = i, i + z[i]

        found_fields = {}
        if z[i] == len(pattern):
            text_idx = i - len(pattern) - 1
            found_fields = {"found": list(range(text_idx, text_idx + len(pattern)))}

        steps.append({"step": len(steps)+1,
                      "table": [z[:i+1] + [None]*(n-i-1)],
                      "current": [0, i],
                      **found_fields,
                      "description": f"Z[{i}] = {z[i]}" + (f" → Found pattern at text index {i-len(pattern)-1}!" if z[i] == len(pattern) else "")})

    return steps


def longest_palindrome(text: str) -> list[dict]:
    steps = []
    n = len(text)
    if n == 0:
        return steps

    start = max_len = 0
    dp = [[False]*n for _ in range(n)]

    for i in range(n):
        dp[i][i] = True

    for i in range(n-1):
        if text[i] == text[i+1]:
            dp[i][i+1] = True
            start, max_len = i, 2

    for length in range(3, n+1):
        for i in range(n - length + 1):
            j = i + length - 1
            if text[i] == text[j] and dp[i+1][j-1]:
                dp[i][j] = True
                if length > max_len:
                    start, max_len = i, length
                steps.append({"step": len(steps)+1,
                              "table": [[1 if dp[r][c] else 0 for c in range(n)] for r in range(n)],
                              "row_headers": list(text), "col_headers": list(text),
                              "current": [i, j],
                              "description": f"Palindrome: '{text[i:j+1]}'"})

    steps.append({"step": len(steps)+1,
                  "description": f"Longest palindrome: '{text[start:start+max_len]}' (length {max_len})"})
    return steps
