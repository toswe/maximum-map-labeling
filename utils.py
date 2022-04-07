import itertools
import math

# TODO Create an Enum instad of global variables
NE = 0
NW = 1
SW = 2
SE = 3

LEFT = 0
RIGHT = 1
DOWN = 2
UP = 3


def _distance_between_points(point1, point2):
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

    point_limits = {
        point: [math.inf, math.inf,
                math.inf, math.inf]
        for point in points
    }

    for point1, point2 in itertools.combinations(points, 2):
        distance = _distance_between_points(point1, point2)
        # TODO cover the cases where point1[0] = point2[0] or point1[1] = point2[1]
        if point1[0] < point2[0]:
            if point1[1] < point2[1]:
                # point2 is north east

                # If point2 is NE from point1 the new limit in the NE direction
                # is the minimum of the old limit and the distance to point2
                point_limits[point1][NE] = min(
                    point_limits[point1][NE], distance)

                # Same thing here but in the oposite direction (SE)
                # and for point2
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
        # Add the limits in all 4 directions to square_sizes_set
        square_sizes_set.update(limit)

        # Add the half of the value of each limit
        # (In the case when two points limits are "pointing"
        # twoards each other (eg. one is NE and the other one is SW)
        # they can meet half way)
        square_sizes_set.update(x / 2 for x in limit)
        max_size = min(max(limit), max_size)

    # TODO optimize list reduction
    #  (maybe write a sort function that discards values larger then max_size)
    square_sizes_list = sorted(list(
        size for size in square_sizes_set if size <= max_size
    ))
    return square_sizes_list


def _get_edges(point, square_orientation, square_size):
    """
    A function that finds the 4 edges of the square.

    Since the square is paralel to the x and y axis,
    the edges can be represented by 4 lines that are
    also paralel to the axis.

    Since we know the angle of the lines the only other
    thing needed to fix them in space is a dot
    that they contain.

    Returns:
        A list of 4 points ([x1, x2, y1, y2])

        The first two are on the x axis,
        for the two lines paralel to the y axis,
        and the second two are on the y axis,
        for the two lines paralel to the x axis.

    """
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
    """
    Checks if two sqares are overlaping.

    """
    first_edges = _get_edges(
        first_point, first_square_orientation, square_size
    )
    second_edges = _get_edges(
        second_point, second_square_orientation, square_size
    )

    if first_edges[LEFT] < second_edges[RIGHT] and \
            first_edges[RIGHT] > second_edges[LEFT] and \
            first_edges[UP] > second_edges[DOWN] and \
            first_edges[DOWN] < second_edges[UP]:
        return True
    return False


def binary_search(squre_sizes, points, find_placing):
    """
    Args:
        squre_sizes - a list of possible sqare sizes (list(float))
        points - a list of float pairs ( list( (float, float) ) )
        find_placings - a function that takes a list of points,
            and a square size, and returns a valid square placement
            or False if there is no valid placement (see searchses.py)

    Returns:
        optimal_square_size - float
        points_and_their_orientation - list( ((float, float), int) )

    """
    l_bound = 0
    u_bound = len(squre_sizes) - 1

    best_placing = find_placing(points, squre_sizes[u_bound])
    if best_placing:
        return u_bound, list(zip(points, best_placing))

    best_placing = find_placing(points, squre_sizes[l_bound])

    while True:
        m_bound = int((l_bound + u_bound) / 2)
        placing = find_placing(points, squre_sizes[m_bound])
        if placing:
            best_placing = placing
            l_bound = m_bound
        else:
            u_bound = m_bound
        if u_bound - l_bound <= 1:
            break

    optimal_square_size = squre_sizes[l_bound]
    points_and_their_orientation = list(zip(points, best_placing))

    return optimal_square_size, points_and_their_orientation
