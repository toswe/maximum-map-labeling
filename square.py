ORIENTATIONS = {'ne', 'nw', 'sw', 'se'}


class Square:
    def __init__(self, point, orientation, size) -> None:
        if orientation not in ORIENTATIONS:
            raise f"Wrong sqaure orientation '{orientation}'."

        if orientation[0] == 'n':
            self.edge_up = point.y + size
            self.edge_down = point.y
        else:
            self.edge_up = point.y
            self.edge_down = point.y - size

        if orientation[1] == 'e':
            self.edge_right = point.y + size
            self.edge_left = point.y
        else:
            self.edge_right = point.y
            self.edge_left = point.y - size


    def __str__(self) -> str:
        return "(x: {:.2f} {:.2f}, y: {:.2f} {:.2f})".format(
            self.edge_left, self.edge_right, self.edge_down, self.edge_up
        )


    def has_overlap(self, square):
        if self.edge_left < square.edge_right and \
            self.edge_right > square.edge_left and \
            self.edge_up > square.edge_down and \
            self.edge_down < square.edge_up:
            return True
        return False