import os
import sys

from cellular import cellular


def main():

    colors = ['black', 'blue', 'yellow', 'orange', 'red']

    ca = cellular.TotalisticCellularAutomaton(400, colors=colors, radius=1, states=5)

    base = str(ca)
    cas_folder = 'tmp/{}/'.format(base)

    try:
        os.mkdir(cas_folder)
    except FileExistsError:
        return
    sys.stdout = open(cas_folder + 'data.txt', 'w')
    f = sys.stderr
    j = 1

    while any(rule != 0 for rule in ca.rules):
        ca.reseed()
        ca.run(800)
        print(j)
        ca.print_stats()

        image = ca.draw()

        image.save(cas_folder + '{}-{}.png'.format(base, j))
        ca.decimate()
        print()
        j += 1
        f.write(str(j))


if __name__ == '__main__':
    for i in range(0, 20):
        main()


