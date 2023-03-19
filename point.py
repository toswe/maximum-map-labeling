import math


class Point:
    def __init__(self ,x, y):
        self.x = x
        self.y = y
        self.ne = math.inf
        self.nw = math.inf
        self.se = math.inf
        self.sw = math.inf
    
    def distance(self, point): 
        return min(abs(self.x - point.x), abs(self.y - point.y))
    
    def __eq__(self, point):
        if isinstance(point, Point):
            return self.x == point.x and self.y == point.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))
