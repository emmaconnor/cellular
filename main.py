import csv
import os
import os.path as path

from cellular import cellular

def do_run(csv_writer, cas_folder, i, n):
    'do run i of n'
    colors = ['black', 'blue', 'yellow', 'orange', 'red']
    ca = cellular.TotalisticCellularAutomaton(400, colors=colors, radius=1, states=5)

    base = str(ca)
    ca_folder = path.join(cas_folder, base)

    try:
        os.mkdir(ca_folder)
    except FileExistsError:
        pass


    j = 0
    while any(rule != 0 for rule in ca.rules):
        ca.reseed()
        ca_class = ca.run(800)
        ca.print_stats()
        print()

        image = ca.draw()
        image.save(path.join(ca_folder, '{:02d}-{}.png'.format(j, ca)))

        if ca_class is not None:
            print("Detected class {}".format(ca_class))
        else:
            image.show()
            while True:
                answer = input("Class: ")
                if answer in ('1', '2', '3', '4'):
                    break
                else:
                    ca.resume(800)
                    image = ca.draw()
                    image.show()

            ca_class = int(answer)

        csv_writer.writerow([base, str(ca), j, ca_class, ca.lam, ca.lam_t, ca.entropy, ca.entropy_t, ca.entropy_p, ca.entropy_a])

        ca.decimate()
        j += 1


def main():
    n_runs = 40

    cas_folder = 'tmp/'


    try:
        os.mkdir(cas_folder)
    except FileExistsError:
        pass

    csv_file = open(path.join(cas_folder, 'data.csv'), 'w', newline='')
    csv_writer = csv.writer(csv_file)

    for i in range(n_runs):
        do_run(csv_writer, cas_folder, i, n_runs)

    csv_file.close()








if __name__ == '__main__':
    main()


