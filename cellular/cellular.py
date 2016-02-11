import collections
import itertools
import random

from .util import util

from fractions import Fraction
from PIL import Image, ImageDraw
from math import log2


class TotalisticCellularAutomaton:
    def __init__(self, width, states=5, radius=1, colors=None, rules=None):
        self.n_cells = width
        self.n_states = states
        self.radius = radius

        if colors is None:
            self.colors = [util.randcolor() for _ in range(self.n_states)]
        else:
            if len(colors) != self.n_states:
                raise ValueError("Invalid number of colors. Expected {}.".format(self.n_states))
            self.colors = colors

        self.reseed()

        n_rules = (2*self.radius + 1) * (self.n_states - 1) + 1
        if rules is None:
            self.rules = [0] + [random.randrange(1, self.n_states) for _ in range(n_rules - 1)]
        else:
            if len(rules) != n_rules:
                raise ValueError("Invalid number of rules. Expected {}.".format(n_rules))
            self.rules = rules

    def run(self, ngens):
        for n in range(ngens):
            c = self.next_gen()
            if c is not None:
                return c

    def resume(self, ngens):
        self.history = [self.history[-1]]
        self.history_set = {tuple(self.history[0])}
        self.run(ngens)
        

    def draw(self):
        n = len(self.history)
        m = len(self.history[0])

        image = Image.new('RGB', (m, n))
        draw = ImageDraw.Draw(image)

        for i in range(n):
            for j in range(m):
                state = self.history[i][j]
                draw.point((j, i), fill=self.colors[state])

        return image

    def print_stats(self):
        print('[' + ' '.join(str(r) for r in self.rules) + ']')
        print(("{:10s}    " * 6).format('lambda', 'lambda_t', 'entropy', 'entropy_t', 'entropy_p', 'entropy_a'))
        print(("{:10.8f}    " * 6).format(self.lam, self.lam_t, self.entropy, self.entropy_t, self.entropy_p, self.entropy_a))
        
    def neighbor_sum(self, pos):
        return sum(self.cells[(pos+i)%self.n_cells] for i in range(-self.radius, self.radius+1))
            
    def next_gen(self):
        self.cells = [self.rules[self.neighbor_sum(i)] for i in range(self.n_cells)]
        if self.cells == self.history[-1]:
            return 1
        elif tuple(self.cells) in self.history_set:
            return 2
        self.history.append(self.cells)
        self.history_set.add(tuple(self.cells))

    def decimate(self):
        nonzeroes = [i for i in range(len(self.rules)) if self.rules[i] != 0]
        if len(nonzeroes) != 0:
            self.rules[random.choice(nonzeroes)] = 0

    def reseed(self):
        self.cells = [random.randrange(0, self.n_states) for _ in range(self.n_cells)]
        self.history = [self.cells]
        self.history_set = {tuple(self.cells)}

    @property
    def lam(self):
        """Currently only works with machines of radius 1 and 5 states"""
        N = 2*self.radius + 1
        T = pow(self.n_states, 2*self.radius +1)
        def n(s):
            tot = 0
            for i in range(0, len(self.rules)):
                if self.rules[i] == s:
                    tot += util.C(N, i, self.n_states-1)
            return tot

        return 1.0 - n(0) / T

    @property
    def lam_t(self):
        return 1.0 - self.rules.count(0) / len(self.rules)

    @property
    def entropy(self):
        N = 2*self.radius + 1
        def n(s):
            tot = 0
            for i in range(0, len(self.rules)):
                if self.rules[i] == s:
                    tot += util.C(N, i, self.n_states-1)
            return tot
        ent = 0
        for i in range(0, self.n_states):
            p_s = n(i) / pow(self.n_states, N)
            if p_s == 0:
                continue
            else:
                ent += p_s * log2(p_s)
        return -1 * ent

    @property
    def entropy_t(self):
        probs = [self.rules.count(state) / len(self.rules) for state in range(self.n_states)]
        return -sum(p*log2(p) for p in probs if p != 0)

    def get_probs(self, iters=5):
        N = self.radius*2 + 1

        probs = [Fraction(1, self.n_states) for _ in range(self.n_states)]

        for x in range(iters):
            new_probs = [0 for _ in probs]
            for neighborhood in itertools.product(*[range(self.n_states) for _ in range(N)]):
                p_n = util.product(probs[state] for state in neighborhood)
                new_state = self.rules[sum(neighborhood)]
                new_probs[new_state] += p_n
            probs = new_probs

        return [float(p) for p in probs]

    @property
    def entropy_p(self):
        return -sum(p*log2(p) for p in self.get_probs() if p != 0)

    @property
    def entropy_a(self):
        return -sum(p*log2(p) for p in self.get_real_probs() if p != 0)

    def get_real_probs(self):
        total = len(self.history) * len(self.history[0])

        c = collections.Counter()
        for row in self.history:
            c.update(row)
        probs = [c[state]/total for state in range(self.n_states)]
        return probs

    def __str__(self):
        return ''.join(str(r) for r in self.rules)


