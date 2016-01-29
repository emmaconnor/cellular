import cellular
import util

from PIL import Image, ImageDraw

        
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

    ca = cellular.TotalisticCellularAutomaton()

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
        print(util.format_floats(get_real_probs(ca, history)))
        classification = None

        while classification not in ('1', '2', '3', '4'):
            classification = input("Class: ")

        image.save(cas_folder + '{}-{}-{}.png'.format(base, ca, classification))

        ca.decimate()


if __name__ == '__main__':
    main()


