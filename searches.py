import itertools

import utils


def _brute_test(points, square_size, square_placings):
    for first, second in itertools.combinations(range(len(points)), 2):
        if utils.check_overlap(points[first], square_placings[first], points[second], square_placings[second], square_size):
            return False
    return True


def brute_force(points, square_size):
    for square_placings in itertools.product([utils.NE, utils.NW, utils.SW, utils.SE], repeat=len(points)):
        if _brute_test(points, square_size, square_placings):
            return square_placings
    return ()


def moj_src():
    pass
