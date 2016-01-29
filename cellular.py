import collections
import itertools
import random

import util

from fractions import Fraction


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

        cache = {}
        def D(k, n):
            if (k, n) in cache: return cache[k, n]
            if n == 1:
                result = 1 if k < K else 0
            elif k < K:
                result = util.choose(n + k - 1, k)
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
            print(util.format_floats([float(p) for p in probs]))
            new_probs = [0 for _ in probs]
            for neighborhood in itertools.product(*[range(self.n_states) for _ in range(N)]):
                p_n = product(probs[state] for state in neighborhood)
                new_state = self.rules[sum(neighborhood)]
                new_probs[new_state] += p_n
            probs = new_probs

        return probs

    def __str__(self):
        return ''.join(str(r) for r in self.rules)


