import cellular
import util

def get_classification():
    answer = None

    while answer not in ('1', '2', '3', '4'):
        answer = input("Class: ")

    return answer


def main():
    cas_folder = 'cas/'
    colors = ['black', 'blue', 'yellow', 'orange', 'red']

    ca = cellular.TotalisticCellularAutomaton(400, colors=colors)

    base = str(ca)

    while any(rule != 0 for rule in ca.rules):
        ca.reseed()
        ca.run(800)
        ca.print_stats()

        image = ca.draw()
        image.show()

        classification = get_classification()

        image.save(cas_folder + '{}-{}-{}.png'.format(base, ca, classification))
        ca.decimate()
        print()


if __name__ == '__main__':
    main()


