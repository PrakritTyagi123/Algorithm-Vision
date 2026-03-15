"""Mathematical Algorithms with step-by-step visualization."""


def euclidean_gcd(a: int, b: int) -> list[dict]:
    steps = []
    while b:
        steps.append({"step": len(steps)+1,
                      "table": [[a, b, a % b]],
                      "col_headers": ["a", "b", "a mod b"],
                      "description": f"gcd({a}, {b}): {a} mod {b} = {a % b}"})
        a, b = b, a % b
    steps.append({"step": len(steps)+1,
                  "table": [[a, 0, a]],
                  "col_headers": ["a", "b", "gcd"],
                  "description": f"GCD = {a}"})
    return steps


def sieve_of_eratosthenes(n: int) -> list[dict]:
    steps = []
    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False
    primes = []

    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            composites = []
            for j in range(i*i, n + 1, i):
                is_prime[j] = False
                composites.append(j)
            steps.append({"step": len(steps)+1,
                          "table": [[1 if is_prime[k] else 0 for k in range(n+1)]],
                          "col_headers": [str(k) for k in range(n+1)],
                          "current": [0, i],
                          "highlighted": [[0, c] for c in composites[:20]],
                          "description": f"Prime {i}: mark multiples {composites[:10]}{'...' if len(composites)>10 else ''}"})

    steps.append({"step": len(steps)+1,
                  "description": f"Primes up to {n}: {primes}"})
    return steps


def fast_exponentiation(base: int, exp: int, mod: int = None) -> list[dict]:
    steps = []
    result = 1
    b = base
    e = exp

    while e > 0:
        if e % 2 == 1:
            result = result * b if mod is None else (result * b) % mod
            steps.append({"step": len(steps)+1,
                          "table": [[b, e, result]],
                          "col_headers": ["base", "exp", "result"],
                          "description": f"exp is odd: result = result × {b} = {result}"})
        b = b * b if mod is None else (b * b) % mod
        e //= 2
        if e > 0:
            steps.append({"step": len(steps)+1,
                          "table": [[b, e, result]],
                          "col_headers": ["base", "exp", "result"],
                          "description": f"Square base: {b}, halve exp: {e}"})

    steps.append({"step": len(steps)+1,
                  "description": f"{base}^{exp}" + (f" mod {mod}" if mod else "") + f" = {result}"})
    return steps


def modular_inverse(a: int, m: int) -> list[dict]:
    steps = []

    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        steps.append({"step": len(steps)+1,
                      "table": [[a, b, gcd, x, y]],
                      "col_headers": ["a", "b", "gcd", "x", "y"],
                      "description": f"ext_gcd({a}, {b}) → gcd={gcd}, x={x}, y={y}"})
        return gcd, x, y

    gcd, x, _ = extended_gcd(a % m, m)
    if gcd != 1:
        steps.append({"step": len(steps)+1,
                      "description": f"Modular inverse doesn't exist (gcd={gcd})"})
    else:
        inv = (x % m + m) % m
        steps.append({"step": len(steps)+1,
                      "description": f"Modular inverse of {a} mod {m} = {inv}"})
    return steps


def prime_factorization(n: int) -> list[dict]:
    steps = []
    original = n
    factors = []
    d = 2

    while d * d <= n:
        while n % d == 0:
            factors.append(d)
            steps.append({"step": len(steps)+1,
                          "table": [[n, d, n // d]],
                          "col_headers": ["n", "factor", "n/factor"],
                          "description": f"{n} ÷ {d} = {n // d}"})
            n //= d
        d += 1

    if n > 1:
        factors.append(n)
        steps.append({"step": len(steps)+1,
                      "table": [[n, n, 1]],
                      "col_headers": ["n", "factor", "n/factor"],
                      "description": f"Remaining prime: {n}"})

    steps.append({"step": len(steps)+1,
                  "description": f"{original} = {' × '.join(map(str, factors))}"})
    return steps
