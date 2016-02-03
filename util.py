import colorsys
import random

def randcolor():
    hue = random.random()
    sat = random.randint(700, 1000) / 1000
    val = random.randint(700, 1000) / 1000
    return tuple(int(f*255) for f in colorsys.hsv_to_rgb(hue, sat, val))

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


def format_floats(floats):
    fstr = '  '.join('{:10.08f}' for _ in floats)
    return fstr.format(*floats)


