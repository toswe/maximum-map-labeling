import itertools

ORIENTATIONS = ['ne', 'nw', 'sw', 'se']
OPPOSITE_ORIENTATIONS = {'ne' : 'sw', 'nw' : 'se', 'sw' : 'ne', 'se' : 'nw'}


class ProtoSquare:
    def __init__(self, point, orientation) -> None:
        self.point = point
        self.orientation = orientation

class Square:
    def __init__(self, point, orientation, size) -> None:
        self.point = point
        self.orientation = orientation
        self.size = size

        if orientation not in ORIENTATIONS:
            raise Exception(f"Wrong sqaure orientation '{orientation}'.")

        if orientation[0] == 'n':
            self.edge_up = point.y + size
            self.edge_down = point.y
        else:
            self.edge_up = point.y
            self.edge_down = point.y - size

        if orientation[1] == 'e':
            self.edge_right = point.x + size
            self.edge_left = point.x
        else:
            self.edge_right = point.x
            self.edge_left = point.x - size

    def __str__(self) -> str:
        return f"({self.point}, '{self.orientation}')"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.point, self.orientation, self.size))

    def __eq__(self, square):
        return (
                isinstance(square, Square)
            and self.point == square.point
            and self.orientation == square.orientation
            and self.size == square.size
        )

    def has_overlap(self, square):
        return (
                self.edge_left  < square.edge_right
            and self.edge_right > square.edge_left
            and self.edge_up    > square.edge_down
            and self.edge_down  < square.edge_up
        )

    def has_point(self, point):
        return (
                self.edge_down < point.y < self.edge_up
            and self.edge_left < point.x < self.edge_right
        )

    def touches(self, square):
        return (
                self.edge_left  == square.edge_right
            or 	self.edge_right == square.edge_left
            or 	self.edge_up    == square.edge_down
            or 	self.edge_down  == square.edge_up
        )

    def get_opposite_orientation(self):
        return OPPOSITE_ORIENTATIONS[self.orientation]

    def plot(self, subplot):
        subplot.scatter([self.point.x], [self.point.y])
        subplot.plot(
            [self.edge_left, self.edge_right, self.edge_right, self.edge_left, self.edge_left],
            [self.edge_down, self.edge_down, self.edge_up, self.edge_up, self.edge_down],
        )

    @staticmethod
    def from_proto(proto_square, size):
        return Square(proto_square.point, proto_square.orientation, size)

    @staticmethod
    def check_overlap(squares):
        for first, second in itertools.combinations(squares, 2):
            if first.has_overlap(second):
                return True
        return False

    @staticmethod
    def get_no_overlap_length(squares):
        length = 0
        for first, second in itertools.combinations(squares, 2):
            if first.has_overlap(second):
                break
            length += 1
        return length
