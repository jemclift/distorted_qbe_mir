import numpy as np
import math
import matplotlib.pyplot as plt

class Hough:

    def __init__(self, database_xs, sample_ys):
        self.xs = database_xs
        self.ys = sample_ys


    def get_line_grad(self, gradient_lower_bound=0.5, gradient_upper_bound=2.0):

        if not self.xs or not self.ys or len(self.xs) != len(self.ys):
            return []

        num_points = len(self.xs)
        accumulator = {}

        for i in range(num_points):

            x = self.xs[i]
            y = self.ys[i]

            num_gradients = 200

            for j in range(num_gradients):

                gradient = gradient_lower_bound + (j / (num_gradients - 1)) * (gradient_upper_bound - gradient_lower_bound)

                rho = y - gradient * x

                quantized_gradient = round(gradient, 2)
                # quantized_gradient = gradient

                if (rho, quantized_gradient) in accumulator:
                    accumulator[(rho, quantized_gradient)] += 1
                else:
                    accumulator[(rho, quantized_gradient)] = 1
        
        def find_lines(accumulator, min_votes):

            lines = []
            # print(f"{len(lines)} line/s, {min_votes} votes")

            for (rho, quantized_gradient), votes in accumulator.items():
                if votes >= min_votes:
                    lines.append((rho, quantized_gradient))

            # fig, ax = plt.subplots(figsize=(8, 6))
            # plt.scatter(self.xs, self.ys, label='Data Points', color='blue')  # Plot the original points

            # for rho, gradient in lines:
            #     x_min = min(self.xs)
            #     x_max = max(self.xs)
            #     y_min = gradient * x_min + rho
            #     y_max = gradient * x_max + rho
            #     plt.plot([x_min, x_max], [y_min, y_max], color='red', label=f'Line (m={gradient:.2f})')

            # ax.set_ylim(min(self.ys), max(self.ys))
            # plt.xlabel('X Axis')
            # plt.ylabel('Y Axis')
            # plt.title('Hough Transform - Lines with Limited Gradient')
            # plt.legend()
            # plt.grid(True)
            # plt.show(block=False)  # Show the plot
            # input("press enter to close plot...")
            # plt.close()

            return lines
        
        
        # min_votes = num_points // 3 # start with line supported by at least 1/3 of the points
        min_votes = 15
        last_len_lines = -1
        lines = find_lines(accumulator, min_votes)

        while True:

            if len(lines) > 1:
                min_votes += 1
                # print("too many lines, increasing votes")
            elif len(lines) == 1:
                # print("perfect! one line found, quitting")
                break
            elif len(lines) == 0 and last_len_lines > 1:
                min_votes -= 1
                # print("no lines found, but previously good so decreasing votes and quiting")
                lines = find_lines(accumulator, min_votes)
                break
            elif len(lines) == 0:
                min_votes -= 1
                # print("no lines found, decreasing votes")

            last_len_lines = len(lines)
            lines = find_lines(accumulator, min_votes)

        # print(f"this many lines => {len(lines)}")
        # print(lines)

        return np.mean([l[1] for l in lines])