import collections
import itertools
import random

from fractions import Fraction
from PIL import Image, ImageDraw


class TotalisticCellularAutomaton:
    def __init__(self):
        self.n_cells = 200
        self.n_states = 5
        self.symbols = ' .oO0'
        self.radius = 1

        self.reseed()

        self.colors = ['black', 'blue', 'yellow', 'orange', 'red']

        n_rules = (2*self.radius + 1) * (self.n_states - 1)
        self.rules = [0] + [random.randrange(1, self.n_states) for _ in range(n_rules)]

    def neighbor_sum(self, pos):
        return sum(self.cells[(pos+i)%self.n_cells] for i in range(-self.radius, self.radius+1))
            
    def next_gen(self):
        self.cells = [self.rules[self.neighbor_sum(i)] for i in range(self.n_cells)]

    def print_gen(self):
        print(''.join(self.symbols[state] for state in self.cells))

    def decimate(self):
        nonzeroes = [i for i in range(len(self.rules)) if self.rules[i] != 0]
        if len(nonzeroes) != 0:
            self.rules[random.choice(nonzeroes)] = 0

    def reseed(self):
        self.cells = [random.randrange(0, self.n_states) for _ in range(self.n_cells)]

    @property
    def lam(self):
        K = self.n_states
        N = self.radius*2 + 1

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
        def D(k, n):
            if (k, n) in cache: return cache[k, n]
            if n == 1:
                result = 1 if k < K else 0
            elif k < K:
                result = choose(n + k - 1, k)
            else:
                result = sum(D(k - j, n - 1) for j in range(K))
            cache[k, n] = result
            return result

        n0 = sum(D(N, i) for i in range(len(self.rules)) if self.rules[i] == 0)
        T = K**N
            
        return 1 - n0/T

    @property
    def lam_t(self):
        return 1.0 - self.rules.count(0) / len(self.rules)

    @property
    def entropy(self):
        return 0.0

    @property
    def entropy_t(self):
        return 0.0

    def get_probs(self):
        print("Modeled: ")
        N = self.radius*2 + 1

        probs = [Fraction(1, self.n_states) for _ in range(self.n_states)]

        def product(nums):
            r = 1
            for n in nums:
                r *= n
            return r

        for x in range(5):
            print(format_floats([float(p) for p in probs]))
            new_probs = [0 for _ in probs]
            for neighborhood in itertools.product(*[range(self.n_states) for _ in range(N)]):
                p_n = product(probs[state] for state in neighborhood)
                new_state = self.rules[sum(neighborhood)]
                new_probs[new_state] += p_n
            probs = new_probs

        return probs

    def __str__(self):
        return ''.join(str(r) for r in self.rules)

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
    

        
def draw_history(ca, history):
    n = len(history)
    m = len(history[0])

    image = Image.new('RGB', (m, n))
    draw = ImageDraw.Draw(image)

    for i in range(n):
        for j in range(m):
            state = history[i][j]
            draw.point((j, i), fill=ca.colors[state])

    return image


def main():
    cas_folder = 'cas/'

    ca = TotalisticCellularAutomaton()

    base = str(ca)

    while any(rule != 0 for rule in ca.rules):
        ca.reseed()
        history = [ca.cells]

        for x in range(800):
            ca.next_gen()
            history.append(ca.cells)
            if all(cell == 0 for cell in ca.cells):
                break

        image = draw_history(ca, history)
        image.show()

        print('[' + ' '.join(str(r) for r in ca.rules) + ']')
        print(("{:10s}    " * 4).format('lambda', 'lambda_t', 'entropy', 'entropy_t'))
        print(("{:10.8f}    " * 4).format(ca.lam, ca.lam_t, ca.entropy, ca.entropy_t))
        ca.get_probs()
        print("Actual: ")
        print(format_floats(get_real_probs(ca, history)))
        classification = None

        while classification not in ('1', '2', '3', '4'):
            classification = input("Class: ")

        image.save(cas_folder + '{}-{}-{}.png'.format(base, ca, classification))

        ca.decimate()


if __name__ == '__main__':
    main()

