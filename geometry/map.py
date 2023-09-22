import random
import itertools
import math

from geometry.point import Point
from geometry.square import ORIENTATIONS, OPPOSITE_ORIENTATIONS


def _get_initial_limits():
    return { orientation: math.inf for orientation in ORIENTATIONS }


class Map:
    def __init__(self, num_of_points, size, seed):
        random.seed(seed)

        self.seed = seed
        self.num_of_points = num_of_points
        self.size = size

        self.points = self._generate_points()
        self.limits_of_points = self._get_limits_of_points()
        self.square_size_candidates = self._get_possible_square_sizes()

    def _generate_points(self):
        """
        A function that generates random points with their coordinates and limits
        with Map objet's parametars
        """
        return [
            Point(random.uniform(0, self.size), random.uniform(0, self.size))
            for _ in range(self.num_of_points)
        ]

    def _get_limits_of_points(self):
        limits_of_points = {point: _get_initial_limits() for point in self.points}

        for point1, point2 in itertools.combinations(self.points, 2):
            distance = point1.distance(point2)

            if point1.x == point2.x or point1.y == point2.y:
                continue

            direction = point1.get_direction_of(point2)
            limits_of_points[point1][direction] = min(limits_of_points[point1][direction], distance)

            op_dir = OPPOSITE_ORIENTATIONS[direction]
            limits_of_points[point2][op_dir] = min(limits_of_points[point2][op_dir], distance)

        return limits_of_points

    def _get_possible_square_sizes(self):
        """
        A function that finds all the possible sizes of squares.
        Args:
            point_limits - A dict containing points and their limits (returned by get_point_limits)

        Returns:
            A sorted list of floats representing the possible square sizes.

        """
        square_sizes_set = set()
        max_size = math.inf

        for point_limits in self.limits_of_points.values():
            limit = list(point_limits.values())
            # Add the limits in all 4 directions to square_sizes_set
            square_sizes_set.update(limit)

            # Add the half of the value of each limit
            # (In the case when two points limits are "pointing"
            # twoards each other (eg. one is NE and the other one is SW)
            # they can meet half way)
            square_sizes_set.update(x / 2 for x in limit)
            max_size = min(max(limit), max_size)

        square_sizes_list = sorted(list(square_sizes_set))
        return square_sizes_list[:square_sizes_list.index(max_size) + 1]
