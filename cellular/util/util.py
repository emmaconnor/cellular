import colorsys
import random

def randcolor():
    hue = random.random()
    sat = random.randint(700, 1000) / 1000
    val = random.randint(700, 1000) / 1000
    return tuple(int(f*255) for f in colorsys.hsv_to_rgb(hue, sat, val))

def randcolor_f():
    hue = random.random()
    sat = random.randint(700, 1000) / 1000
    val = random.randint(700, 1000) / 1000
    return tuple(colorsys.hsv_to_rgb(hue, sat, val))

def product(nums):
    r = 1
    for n in nums:
        r *= n
    return r

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

cache = {}
def C(N, k, m): 
    'Counts number of ways N cells with max state m can sum to k'
    if N <= 1:
        return 1 if (m >= k) else 0
    if k >= N*m/2:
        k = N*m - k
    if (N, k, m) in cache:
        return cache[N, k, m]
    result = sum(C(N-1, j, m) for j in range(max(k-m, 0), k+1))
    cache[N, k, m] = result
    return result

def format_floats(floats):
    fstr = '  '.join('{:10.08f}' for _ in floats)
    return fstr.format(*floats)


