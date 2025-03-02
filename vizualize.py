import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TkAgg")


def read_output(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()

    width = int(lines[1].strip())
    height = int(lines[2].strip())
    xmin = float(lines[3].strip())
    xmax = float(lines[4].strip())
    ymin = float(lines[5].strip())
    ymax = float(lines[6].strip())
    iterations = int(lines[7].strip())
    power = int(lines[8].strip())

    data = [list(map(int, line.split())) for line in lines[9:]]
    return np.array(data), width, height, xmin, ymin, xmax, ymax, iterations, power


def visualize(file_name, save_file_name="output_image.png"):
    image, width, height, xmin, ymin, xmax, ymax, iterations, power = read_output(file_name)

    plt.figure(figsize=(10, 10))
    plt.imshow(image, cmap='inferno', extent=(xmin, ymin, xmax, ymax))
    plt.axis('off')
    plt.xticks([])
    plt.yticks([])
    plt.subplots_adjust(left=0, right=1, top=1, bottom=0)

    plt.savefig(save_file_name, bbox_inches='tight', pad_inches=0, dpi=300)
    # plt.show()


if __name__ == "__main__":
    output_file = "output (2).txt"
    visualize(output_file, "fractal_p_4.png")
