import collections
import itertools
import random

from .util import util

from fractions import Fraction
from PIL import Image, ImageDraw


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

        n_rules = (2*self.radius + 1) * (self.n_states - 1)
        if rules is None:
            self.rules = [0] + [random.randrange(1, self.n_states) for _ in range(n_rules)]
        else:
            if len(rules) != n_rules:
                raise ValueError("Invalid number of rules. Expected {}.".format(n_rules))
            self.rules = rules

    def run(self, ngens):
        for n in range(ngens):
            self.next_gen()

    def resume(self, ngens):
        self.history = [self.history[-1]]
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
        print(("{:10s}    " * 4).format('lambda', 'lambda_t', 'entropy', 'entropy_t'))
        print(("{:10.8f}    " * 4).format(self.lam, self.lam_t, self.entropy, self.entropy_t))
        print("Modeled: ")
        print(util.format_floats(self.get_probs()))
        print("Actual: ")
        print(util.format_floats(self.get_real_probs()))
        
    def neighbor_sum(self, pos):
        return sum(self.cells[(pos+i)%self.n_cells] for i in range(-self.radius, self.radius+1))
            
    def next_gen(self):
        self.cells = [self.rules[self.neighbor_sum(i)] for i in range(self.n_cells)]
        self.history.append(self.cells)

    def decimate(self):
        nonzeroes = [i for i in range(len(self.rules)) if self.rules[i] != 0]
        if len(nonzeroes) != 0:
            self.rules[random.choice(nonzeroes)] = 0

    def reseed(self):
        self.cells = [random.randrange(0, self.n_states) for _ in range(self.n_cells)]
        self.history = [self.cells]

    @property
    def lam(self):
        return 0

    @property
    def lam_t(self):
        return 1.0 - self.rules.count(0) / len(self.rules)

    @property
    def entropy(self):
        return 0.0

    @property
    def entropy_t(self):
        return 0.0

    def get_probs(self, iters=5):
        """
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
        """
        return [0.0 for _ in range(self.n_states)]

    def get_real_probs(self):
        total = len(self.history) * len(self.history[0])

        c = collections.Counter()
        for row in self.history:
            c.update(row)
        probs = [c[state]/total for state in range(self.n_states)]
        return probs

    def __str__(self):
        return ''.join(str(r) for r in self.rules)


