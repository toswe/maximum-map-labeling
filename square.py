ORIENTATIONS = {'ne', 'nw', 'sw', 'se'}

OPPOSITE_ORIENTATIONS = {'ne' : 'sw', 'nw' : 'se', 'sw' : 'ne', 'se' : 'nw'}

class Square:
    def __init__(self, point, orientation, size) -> None:
        self.point = point
        self.orientation = orientation
        self.size = size

        if orientation not in ORIENTATIONS:
            raise f"Wrong sqaure orientation '{orientation}'."

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
        return "(x: {:.2f} {:.2f}, y: {:.2f} {:.2f})".format(
            self.edge_left, self.edge_right, self.edge_down, self.edge_up
        )

    def __eq__(self, square):
        if isinstance(square, Square):
            return self.point == square.point and self.orientation == square.orientation and self.size == square.size
        return False

    def __hash__(self):
        return hash((self.point, self.orientation, self.size))

    def has_overlap(self, square):
        if self.edge_left < square.edge_right and \
            self.edge_right > square.edge_left and \
            self.edge_up > square.edge_down and \
            self.edge_down < square.edge_up:
            return True
        return False

    def has_point(self, point):
        if (
                self.edge_down < point.y < self.edge_up
                and self.edge_left < point.x < self.edge_right
        ):
            return True
        return False

    def get_opposite_orientation(self):
        return OPPOSITE_ORIENTATIONS[self.orientation]
