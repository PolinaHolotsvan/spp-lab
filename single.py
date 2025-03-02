from Pyro4 import expose
import time


class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

        print("Inited.")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))

        width, height, xmin, ymin, xmax, ymax, iterations, power = self.read_input()
        start_time = time.time()

        image = Solver.fill_image(width, height, xmin, ymin, xmax, ymax, iterations, power)
        elapsed_time = time.time() - start_time

        self.write_output(image, elapsed_time, width, height, xmin, ymin, xmax, ymax, iterations, power)

        print("Finished in %.4f seconds." % elapsed_time)

    @staticmethod
    def mandelbrot(c, power, max_iter=100):
        z = 0
        for i in range(max_iter):
            z = z ** power + c
            if abs(z) > 2:
                return i
        return 0

    @staticmethod
    @expose
    def fill_image(width, height, xmin, ymin, xmax, ymax, iterations, power):
        image = [[0 for _ in range(width)] for _ in range(height)]
        for x in range(width):
            for y in range(height):
                re = xmin + (float(x) / width) * (xmax - xmin)
                im = ymin + (float(y) / height) * (ymax - ymin)
                image[y][x] = Solver.mandelbrot(complex(re, im), power, iterations)
        return image

    def read_input(self):
        with open(self.input_file_name, 'r') as f:
            width = int(f.readline())
            height = int(f.readline())
            xmin = float(f.readline())
            xmax = float(f.readline())
            ymin = float(f.readline())
            ymax = float(f.readline())
            iterations = int(f.readline())
            power = int(f.readline())
        return width, height, xmin, ymin, xmax, ymax, iterations, power

    def write_output(self, image, elapsed_time, width, height, xmin, ymin, xmax, ymax, iterations, power):
        with open(self.output_file_name, 'w') as f:
            output_text = "Finished in %.4f seconds." % elapsed_time
            f.write(output_text + '\n')

            f.write(str(width) + '\n')
            f.write(str(height) + '\n')
            f.write(str(xmin) + '\n')
            f.write(str(ymin) + '\n')
            f.write(str(xmax) + '\n')
            f.write(str(ymax) + '\n')
            f.write(str(iterations) + '\n')
            f.write(str(power) + '\n')

            for row in image:
                f.write(" ".join(map(str, row)) + '\n')
