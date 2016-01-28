import random

class TotalisticCellularAutomaton:
    def __init__(self):
        self.n_cells = 200
        self.n_states = 5
        self.symbols = ' .oO0'
        self.radius = 1
        self.cells = [random.randrange(0, self.n_states) for _ in range(self.n_cells)]

        n_rules = (2*self.radius + 1) * (self.n_states - 1)
        self.rules = [0] + [random.randrange(0, self.n_states) for _ in range(n_rules)]


    def neighbor_sum(self, pos):
        return sum(self.cells[(pos+i)%self.n_cells] for i in range(-self.radius, self.radius+1))
            
    def next_gen(self):
        self.cells = [self.rules[self.neighbor_sum(i)] for i in range(self.n_cells)]

    def print_gen(self):
        print(''.join(self.symbols[state] for state in self.cells))

def main():
    ca = TotalisticCellularAutomaton()

    print(ca.rules)
    while True:
        ca.print_gen()
        ca.next_gen()


if __name__ == '__main__':
    main()

