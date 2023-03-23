import random
import itertools
import math

from point import Point


def _get_initial_limits():
    return {
        'ne' : math.inf,
        'nw' : math.inf,
        'se' : math.inf,
        'sw' : math.inf,
    }


class Map:
    def __init__(self, num_of_points, map_size, seed):
        random.seed(seed)

        self.num_of_points = num_of_points
        self.map_size = map_size
        # Points is a dict where keys are points, and values are point limits in each direction
        self.points = dict()


        self._generate_points()


    def _update_point_limits(self):
        for point1, point2 in itertools.combinations(self.points.keys, 2):
            distance = point1.distance(point2)

            if point1.x == point2.x or point1.y == point2.y:
                continue

            if point1.x < point2.x:
                if point1.y < point2.y:
                    # point2 is north east
                    self.points[point1]['ne'] = min(self.points[point1]['ne'], distance)
                    self.points[point2]['sw'] = min(self.points[point2]['sw'], distance)
                else:
                    # point2 is south east
                    self.points[point1]['se'] = min(self.points[point1]['se'], distance)
                    self.points[point2]['nw'] = min(self.points[point2]['nw'], distance)
            else:
                if point1.y < point2.y:
                    # point2 is north west
                    self.points[point1]['nw'] = min(self.points[point1]['nw'], distance)
                    self.points[point2]['se'] = min(self.points[point2]['se'], distance)
                else:
                    # point2 is south west
                    self.points[point1]['sw'] = min(self.points[point1]['sw'], distance)
                    self.points[point2]['ne'] = min(self.points[point2]['ne'], distance)


    def _generate_points(self):
        """
        A function that generates random points with their coordinates and limits
        with Map objet's parametars
        
        """

        while len(self.points) < self.num_of_points:
            point = Point(random.uniform(0, self.map_size), random.uniform(0, self.map_size))
            self.points[point] = _get_initial_limits()

        self._update_point_limits()

        return list(self.points)
