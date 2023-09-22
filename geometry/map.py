import random
import itertools
import math

from geometry.point import Point
from geometry.square import ORIENTATIONS


def _get_initial_limits():
    return { orientation: math.inf for orientation in ORIENTATIONS }


class Map:
    def __init__(self, num_of_points, size, seed):
        random.seed(seed)

        self.seed = seed
        self.num_of_points = num_of_points
        self.size = size

        # Points is a dict where keys are points, and values are point limits in each direction
        self.points = []
        self.limits_of_points = dict()

        self._generate_points()
        self._get_limits_of_points()

        self.square_size_candidates = self._get_possible_square_sizes()

    def _get_limits_of_points(self):
        for point1, point2 in itertools.combinations(self.points, 2):
            distance = point1.distance(point2)

            if point1.x == point2.x or point1.y == point2.y:
                continue

            if point1.is_south_of(point2):
                if point1.is_west_of(point2):
                    self.limits_of_points[point1]['ne'] = min(self.limits_of_points[point1]['ne'], distance)
                    self.limits_of_points[point2]['sw'] = min(self.limits_of_points[point2]['sw'], distance)
                else:
                    self.limits_of_points[point1]['se'] = min(self.limits_of_points[point1]['se'], distance)
                    self.limits_of_points[point2]['nw'] = min(self.limits_of_points[point2]['nw'], distance)
            else:
                if point1.is_west_of(point2):
                    self.limits_of_points[point1]['nw'] = min(self.limits_of_points[point1]['nw'], distance)
                    self.limits_of_points[point2]['se'] = min(self.limits_of_points[point2]['se'], distance)
                else:
                    self.limits_of_points[point1]['sw'] = min(self.limits_of_points[point1]['sw'], distance)
                    self.limits_of_points[point2]['ne'] = min(self.limits_of_points[point2]['ne'], distance)

    def _generate_points(self):
        """
        A function that generates random points with their coordinates and limits
        with Map objet's parametars
        
        """

        while len(self.points) < self.num_of_points:
            point = Point(random.uniform(0, self.size), random.uniform(0, self.size))
            self.points.append(point)
            self.limits_of_points[point] = _get_initial_limits()

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
