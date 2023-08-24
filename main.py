import argparse

from matplotlib import pyplot as plt

from map import Map
from searches.brute_force import BruteForce
from searches.b import B

MAP_SIZE = 100.0
SEED = 'aNiceSeed'


def _plot_squares(squares, title):
    subplot = plt.figure().add_subplot()
    subplot.title.set_text(title)
    for square in squares:
        square.plot(subplot)


def main(num_of_points, map_size, seed):
    the_map = Map(num_of_points, map_size, seed)
    points = list((point.x, point.y) for point in the_map.get_points()) # TODO Change this
    print('Generated points:', points)

    # If there exists a square size and placment in which no squares
    # touch each other, that square size cannot be optimal since
    # we can get a better result by increasing the square size
    # until some two squares touch each other.
    # Thus there are a limited number of possible square sizes
    # that can possibly be optimal.

    print('Possible square size candidates:')
    print(len(the_map.square_size_candidates), the_map.square_size_candidates)
    print()

    # We can then do a binary search through those
    # possible square sizes and find the largest one which
    # has a square placing that is valid.

    # opt_bound, opt_placings = utils.binary_search(
    #     square_size_candidates, points, searches_old.brute_force)

    search_algorithms = [
        BruteForce,
        B,
    ]

    for algorithm in search_algorithms:
        search = algorithm(the_map)
        squares = search.binary_search()

        print("Optimal size: {:.2f}".format(squares[0].size))
        print(f"Largest area: {int(squares[0].size ** 2) * len(points)}")
        print("Placings:")
        print(squares)
        print()
        print('#####################################################')
        print()

        _plot_squares(squares, search.__class__.__name__)

    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--points', type = int)
    parser.add_argument('-m', '--map-size', type = float, default = MAP_SIZE)
    parser.add_argument('-s', '--seed', type = str, default = SEED)
    args = parser.parse_args()

    if not args.points:
        print("Please provide the number of points by specifiing the '-p' flag.")
    else:
        main(args.points, args.map_size, args.seed)
