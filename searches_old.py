import itertools

import utils


# TODO Move this to utils
def _test_placings(points, square_size, square_placings):
    """
    Tests if the given placings are valid, for the given square size
    Args:
        points - A set of points ( set( (float, float) ) )
        square_size - size of the square (float)
        square_placings - A list of sqaure orientations for each point
            (orientation can be utils.NE, utils.NW, utils.SW or utils.SE)
    Returns:
        boolean

    """
    for first, second in itertools.combinations(range(len(points)), 2):
        if utils.check_overlap(points[first], square_placings[first], points[second], square_placings[second], square_size):
            return False
    return True


def brute_force(points, square_size):
    """
    A simple algorithm that goes through all the possible combinations
    of square orientations for the points and checks if they're valid.
    """
    for square_placings in itertools.product([utils.NE, utils.NW, utils.SW, utils.SE], repeat=len(points)):
        if _test_placings(points, square_size, square_placings):
            return square_placings
    return False


def moj_src():
    # TODO Implement this...
    pass
