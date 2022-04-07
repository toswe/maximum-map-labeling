import itertools
import math

NE = 0
NW = 1
SW = 2
SE = 3

LEFT = 0
RIGHT = 1
DOWN = 2
UP = 3


def distance_between_points(point1, point2):
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


def get_point_limits(points):
    """
    A function that finds the distance to the nearest point in all four directions for each point.
    Args:
        points - A set of points (float, float)

    Returns:
        point_limits - a dictionary where the key is a point and the value is a list of 4 floats,
        representing the limits of the point in all four possible directions.

    """

    point_limits = {point: [math.inf, math.inf,
                            math.inf, math.inf] for point in points}
    for point1, point2 in itertools.combinations(points, 2):
        distance = distance_between_points(point1, point2)
        # TODO cover the cases where point1[0] = point2[0] and point1[1] = point2[1]
        if point1[0] < point2[0]:
            if point1[1] < point2[1]:
                # point2 is north east
                point_limits[point1][NE] = min(
                    point_limits[point1][NE], distance)
                point_limits[point2][SW] = min(
                    point_limits[point2][SW], distance)
            else:
                # point2 is south east
                point_limits[point1][SE] = min(
                    point_limits[point1][SE], distance)
                point_limits[point2][NW] = min(
                    point_limits[point2][NW], distance)
        else:
            if point1[1] < point2[1]:
                # point2 is north west
                point_limits[point1][NW] = min(
                    point_limits[point1][NW], distance)
                point_limits[point2][SE] = min(
                    point_limits[point2][SE], distance)
            else:
                # point2 is south west
                point_limits[point1][SW] = min(
                    point_limits[point1][SW], distance)
                point_limits[point2][NE] = min(
                    point_limits[point2][NE], distance)
    return point_limits


def get_possible_square_sizes(point_limits):
    """
    A function that finds all the possible sizes of squares.
    Args:
        point_limits - A dict containing points and their limits (returned by get_point_limits)

    Returns:
        A sorted list of floats representing the possible square sizes.

    """
    square_sizes_set = set()
    max_size = math.inf
    for limit in point_limits.values():
        square_sizes_set.update(limit)
        square_sizes_set.update(x / 2 for x in limit)
        max_size = min(max(limit), max_size)
    # TODO optimize list reduction
    #  (maybe write a sort function that discards values larger then max_size)
    square_sizes_list = sorted(
        list(size for size in square_sizes_set if size <= max_size))
    return square_sizes_list


def _get_edges(point, square_orientation, square_size):
    if square_orientation == NE:
        return [point[0], point[0] + square_size, point[1], point[1] + square_size]
    if square_orientation == NW:
        return [point[0] - square_size, point[0], point[1], point[1] + square_size]
    if square_orientation == SW:
        return [point[0] - square_size, point[0], point[1] - square_size, point[1]]
    if square_orientation == SE:
        return [point[0], point[0] + square_size, point[1] - square_size, point[1]]
    raise Exception('Wrong square orientation.')


def check_overlap(first_point, first_square_orientation, second_point, second_square_orientation, square_size):
    first_edges = _get_edges(
        first_point, first_square_orientation, square_size)
    second_edges = _get_edges(
        second_point, second_square_orientation, square_size)

    if first_edges[LEFT] < second_edges[RIGHT] and first_edges[RIGHT] > second_edges[LEFT] and \
            first_edges[UP] > second_edges[DOWN] and first_edges[DOWN] < second_edges[UP]:
        return True
    return False
