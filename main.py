import os

from cellular import cellular


def main():
    cas_folder = 'tmp/'

    try:
        os.mkdir(cas_folder)
    except FileExistsError:
        pass

    colors = ['black', 'blue', 'yellow', 'orange', 'red']

    ca = cellular.TotalisticCellularAutomaton(400, colors=colors, radius=1, states=5)

    base = str(ca)

    while any(rule != 0 for rule in ca.rules):
        ca.reseed()
        ca.run(800)
        ca.print_stats()

        image = ca.draw()
        image.show()


        while True:
            answer = input("Class: ")
            if answer in ('1', '2', '3', '4'):
                break
            else:
                ca.resume(800)
                image = ca.draw()
                image.show()

        image.save(cas_folder + '{}-{}-{}.png'.format(base, ca, answer))
        ca.decimate()
        print()


if __name__ == '__main__':
    main()


