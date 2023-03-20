ORIENTATIONS = {'ne', 'nw', 'sw', 'se'}


class Square:
    def __init__(self, point, orientation, size) -> None:
        if orientation not in ORIENTATIONS:
            raise f"Wrong sqaure orientation '{orientation}'."

        if orientation[1] == 'e':
            self.edge_up = point.x + size
            self.edge_down = point.x
        else:
            self.edge_up = point.x
            self.edge_down = point.x - size

        if orientation[0] == 'n':
            self.edge_left = point.y + size
            self.edge_right = point.y
        else:
            self.edge_left = point.y
            self.edge_right = point.y - size


    def has_overlap(self, square):
        if self.edge_left < square.edge_right and \
            self.edge_right > square.edge_left and \
            self.edge_up > square.edge_down and \
            self.edge_down < square.edge_up:
            return True
        return False
