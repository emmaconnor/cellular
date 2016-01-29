def choose(n, k):
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0

def format_floats(floats):
    fstr = '  '.join('{:10.08f}' for _ in floats)
    return fstr.format(*floats)


def get_real_probs(ca, history):
    total = len(history) * len(history[0])

    c = collections.Counter()
    for row in history:
        c.update(row)
    probs = [c[state]/total for state in range(ca.n_states)]
    return probs
