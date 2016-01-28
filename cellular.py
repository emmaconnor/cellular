import random

from PIL import Image, ImageDraw


class TotalisticCellularAutomaton:
    def __init__(self):
        self.n_cells = 200
        self.n_states = 5
        self.symbols = ' .oO0'
        self.radius = 1
        self.cells = [random.randrange(0, self.n_states) for _ in range(self.n_cells)]

        self.colors = ['black', 'blue', 'yellow', 'orange', 'red']

        n_rules = (2*self.radius + 1) * (self.n_states - 1)
        self.rules = [0] + [random.randrange(0, self.n_states) for _ in range(n_rules)]

    def neighbor_sum(self, pos):
        return sum(self.cells[(pos+i)%self.n_cells] for i in range(-self.radius, self.radius+1))
            
    def next_gen(self):
        self.cells = [self.rules[self.neighbor_sum(i)] for i in range(self.n_cells)]

    def print_gen(self):
        print(''.join(self.symbols[state] for state in self.cells))

        
def draw_history(ca, history):
    n = len(history)
    m = len(history[0])

    image = Image.new('RGB', (m, n))
    draw = ImageDraw.Draw(image)

    for i in range(n):
        for j in range(m):
            state = history[i][j]
            draw.point((j, i), fill=ca.colors[state])

    image.show()

        

def main():
    ca = TotalisticCellularAutomaton()

    print(ca.rules)

    history = [ca.cells]
    for x in range(1000):
        ca.next_gen()
        history.append(ca.cells)

    draw_history(ca, history)


if __name__ == '__main__':
    main()

