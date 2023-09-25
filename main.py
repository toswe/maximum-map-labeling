import argparse

from matplotlib import pyplot as plt

from geometry.map import Map
from searches.brute_force import BruteForce
from searches.brute_force_cache import BruteForceCache
from searches.b import B
from searches.genetic import Genetic

MAP_SIZE = 100.0
SEED = 42


def _plot_squares(squares, title):
    subplot = plt.figure().add_subplot()
    subplot.title.set_text(title)
    for square in squares:
        square.plot(subplot)


def main(num_of_points, map_size, seed):
    the_map = Map(num_of_points, map_size, seed)
    print('Generated points:', the_map.points)
    print()
    print(f'There are {len(the_map.square_size_candidates)} possible square size candidates:')
    print(the_map.square_size_candidates)
    print()

    search_algorithms = [
        # BruteForce,
        # BruteForceCache,
        # B,
        Genetic,
    ]

    for algorithm in search_algorithms:
        search = algorithm(the_map)
        squares, elapsed = search.search_with_time_measure()

        print("Results of the {} algorithm are:".format(search.__class__.__name__))
        print("Time elapsed: {:.2f}s".format(elapsed))
        print("Optimal size: {:.2f}".format(squares[0].size))
        print("Largest area: {:.2f}".format(squares[0].size ** 2 * num_of_points))
        print()
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
