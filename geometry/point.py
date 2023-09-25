class Point:
    def __init__(self ,x, y):
        self.x = x
        self.y = y
        self.squares = [] # TODO Move this

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

    def distance(self, point):
        return max(abs(self.x - point.x), abs(self.y - point.y))

    def is_south_of(self, point):
        return self.x < point.x

    def is_west_of(self, point):
        return self.y < point.y

    def get_direction_of(self, point):
        return (
            ('n' if self.is_south_of(point) else 's')
            + ('e' if self.is_west_of(point) else 'w')
        )
