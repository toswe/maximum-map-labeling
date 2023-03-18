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
