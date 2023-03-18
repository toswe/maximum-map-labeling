from point import Point
import random
import itertools

class Map:
    def __init__(self, num_of_points, map_size, seed):
        self.num_of_points = num_of_points
        self.map_size = map_size
        self.seed = seed
        self.points = set()

    def _update_limits(self):
        
        for point1, point2 in itertools.combinations(self.points, 2):
            distance = point1.distance(point2)
            if point1.x < point2.x:
                if point1.y < point2.y:
                    # point2 is north east
                    point1.ne = min(point1.ne, distance)
                    point2.sw = min(point2.sw, distance)
                else:
                    # point2 is south east
                    point1.se = min(point1.se, distance)
                    point2.nw = min(point2.nw, distance)
            else:
                if point1.y < point2.y:
                    # point2 is north west
                    point1.nw = min(point1.nw, distance)
                    point2.se = min(point2.se, distance)
                else:
                    # point2 is south west
                    point1.sw = min(point1.sw, distance)
                    point2.ne = min(point2.ne, distance)



    def generate(self):
        """
        A function that generates random points with their coordinates and limits
        with Map objet's parametars
        
        """
        random.seed(self.seed)
        i = 0
        while i < self.num_of_points:
            point = Point(random.uniform(0, self.map_size), random.uniform(0, self.map_size))
            if point in self.points:
                continue
            else:
                self.points.add(point)
                i += 1

        self._update_limits()

        return list(self.points)
