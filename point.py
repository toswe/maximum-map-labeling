class Point:
    def __init__(self ,x, y):
        self.x = x
        self.y = y


    def distance(self, point): 
        return max(abs(self.x - point.x), abs(self.y - point.y))
    

    def __eq__(self, point):
        if isinstance(point, Point):
            return self.x == point.x and self.y == point.y
        return False


    def __hash__(self):
        return hash((self.x, self.y))


    def __repr__(self):
        return "(x: {:.2f}, y: {:.2f})".format(self.x, self.y)


    def __str__(self):
        return "(x: {:.2f}, y: {:.2f})".format(self.x, self.y)
