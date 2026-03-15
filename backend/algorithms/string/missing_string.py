"""Missing String Algorithms with step-by-step visualization."""


def manachers_algorithm(text: str) -> list[dict]:
    steps = []
    t = '^#' + '#'.join(text) + '#$'
    n = len(t)
    p = [0] * n
    c = r = 0
    text_row = [ord(ch) for ch in text]

    for i in range(1, n - 1):
        mirror = 2 * c - i
        if i < r:
            p[i] = min(r - i, p[mirror])

        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1

        if i + p[i] > r:
            c, r = i, i + p[i]

        if p[i] > 0:
            orig_center = (i - 1) // 2
            orig_len = p[i]
            lo = max(0, orig_center - orig_len // 2)
            hi = min(len(text) - 1, orig_center + orig_len // 2)
            steps.append({
                "step": len(steps) + 1,
                "table": [text_row],
                "col_headers": list(text),
                "current": [0, orig_center],
                "highlighted": [[0, j] for j in range(lo, hi + 1)],
                "description": f"Center {orig_center}: palindrome radius={orig_len}",
            })

    max_len = max(p)
    center_idx = p.index(max_len)
    start = (center_idx - max_len) // 2
    longest = text[start:start + max_len]

    steps.append({"step": len(steps) + 1,
                  "table": [text_row],
                  "col_headers": list(text),
                  "description": f"Longest palindrome: '{longest}' (length {max_len})"})
    return steps


def aho_corasick(text: str, patterns: list[str]) -> list[dict]:
    steps = []
    from collections import deque

    # Build trie
    goto = [{}]
    fail = [0]
    output = [[]]

    for pid, pattern in enumerate(patterns):
        state = 0
        for ch in pattern:
            if ch not in goto[state]:
                goto.append({})
                fail.append(0)
                output.append([])
                goto[state][ch] = len(goto) - 1
            state = goto[state][ch]
        output[state].append(pid)
        steps.append({"step": len(steps) + 1,
                      "description": f"Add pattern '{pattern}' to trie (state {state})"})

    # Build failure links
    queue = deque()
    for ch, s in goto[0].items():
        fail[s] = 0
        queue.append(s)

    while queue:
        r = queue.popleft()
        for ch, s in goto[r].items():
            queue.append(s)
            state = fail[r]
            while state != 0 and ch not in goto[state]:
                state = fail[state]
            fail[s] = goto[state].get(ch, 0)
            if fail[s] == s:
                fail[s] = 0
            output[s] = output[s] + output[fail[s]]

    steps.append({"step": len(steps) + 1,
                  "description": f"Automaton built: {len(goto)} states, {len(patterns)} patterns"})

    # Search
    state = 0
    matches = []
    for i, ch in enumerate(text):
        while state != 0 and ch not in goto[state]:
            state = fail[state]
        state = goto[state].get(ch, 0)

        steps.append({"step": len(steps) + 1,
                      "current": [0, i],
                      "description": f"text[{i}]='{ch}', state={state}"})

        if output[state]:
            for pid in output[state]:
                start = i - len(patterns[pid]) + 1
                matches.append((start, patterns[pid]))
                steps.append({"step": len(steps) + 1,
                              "found": list(range(start, i + 1)),
                              "description": f"Found '{patterns[pid]}' at index {start}"})

    steps.append({"step": len(steps) + 1,
                  "description": f"Total matches: {len(matches)}"})
    return steps


def suffix_tree_demo(text: str) -> list[dict]:
    """Simplified suffix tree visualization using sorted suffixes."""
    steps = []
    text = text + "$"
    n = len(text)
    text_row = [ord(c) for c in text]

    steps.append({"step": len(steps) + 1,
                  "table": [text_row],
                  "col_headers": list(text),
                  "description": f"Building suffix tree for '{text}'"})

    suffixes = []
    for i in range(n):
        suffix = text[i:]
        suffixes.append((suffix, i))
        steps.append({"step": len(steps) + 1,
                      "table": [text_row],
                      "col_headers": list(text),
                      "current": [0, i],
                      "description": f"Suffix {i}: '{suffix}'"})

    suffixes.sort()

    sa = [idx for _, idx in suffixes]
    lcp_vals = [0] * n

    for i in range(1, len(suffixes)):
        s1, idx1 = suffixes[i - 1]
        s2, idx2 = suffixes[i]
        lcp_len = 0
        while lcp_len < min(len(s1), len(s2)) and s1[lcp_len] == s2[lcp_len]:
            lcp_len += 1
        lcp_vals[i] = lcp_len
        if lcp_len > 0:
            steps.append({"step": len(steps) + 1,
                          "table": [sa, lcp_vals],
                          "row_headers": ["SA", "LCP"],
                          "current": [1, i],
                          "description": f"LCP('{s1[:15]}', '{s2[:15]}') = {lcp_len}"})

    steps.append({"step": len(steps) + 1,
                  "table": [sa, lcp_vals],
                  "row_headers": ["SA", "LCP"],
                  "description": f"Suffix tree for '{text}' complete. {n} leaves."})
    return steps
