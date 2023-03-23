import utils
import searches
import argparse

from map import Map

MAP_SIZE = 100.0
SEED = 'aNiceSeed'


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

    square_size_candidates = the_map.get_possible_square_sizes()

    print('Possible square size candidates:')
    print(len(square_size_candidates), square_size_candidates)
    print()

    # We can then do a binary search through those
    # possible square sizes and find the largest one which
    # has a square placing that is valid.
    opt_bound, opt_placings = utils.binary_search(
        square_size_candidates, points, searches.brute_force)

    # opt_bound, opt_placings = binary_search(POINTS, SQUARE_SIZE_CANDIDATES, searches.moj_src)

    print('The largest area of the squares:')
    print((opt_bound ** 2) * len(points))
    print()
    print("Optimal square size and placings:")
    print(opt_bound, opt_placings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--points', type = int)
    parser.add_argument('-m', '--map-size', type = float, default = MAP_SIZE)
    parser.add_argument('-s', '--seed', type = str, default = SEED)
    args = parser.parse_args()
    main(args.points, args.map_size, args.seed)
