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

        y_chunks = []
        chunk_height = height // len(self.workers)
        for i in range(len(self.workers)):
            start = i * chunk_height
            end = (i + 1) * chunk_height if i < len(self.workers) - 1 else height
            y_chunks.append((start, end))

        mapped = []
        start_time = time.time()
        for i in range(len(self.workers)):
            mapped.append(
                    self.workers[i].fill_image_chunk(y_chunks[i], width, height, xmin, ymin, xmax,
                                                     ymax, iterations, power))

        image = []
        for result in mapped:
            image.extend(result.value)

        elapsed_time = time.time() - start_time

        print("Finished in %.4f seconds." % elapsed_time)
        self.write_output(image, elapsed_time, width, height, xmin, ymin, xmax, ymax, iterations, power)

    @expose
    def fill_image_chunk(self, y_chunk, width, height, xmin, ymin, xmax, ymax, iterations, power):
        chunk_start, chunk_end = y_chunk
        chunk_size = chunk_end - chunk_start + 1

        image = [[0 for _ in range(width)] for _ in range(chunk_size)]

        for x in range(width):
            for y in range(chunk_start, chunk_end + 1):
                re = xmin + (float(x) / width) * (xmax - xmin)
                im = ymin + (float(y) / height) * (ymax - ymin)
                image[y - chunk_start][x] = self.mandelbrot(complex(re, im), power, iterations)

        return image

    @staticmethod
    def mandelbrot(c, power, max_iter=100):
        z = 0
        for i in range(max_iter):
            z = z ** power + c
            if abs(z) > 2:
                return i
        return 0

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
            output_text = "Finished in %.4f seconds using %d workers" % (elapsed_time, len(self.workers))
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
