import itertools

from searches.search import Search
from square import Square, ORIENTATIONS


class B(Search):
    def get_conflicts(squares):
        conflicts = dict()
        for sq1, sq2  in itertools.combinations(squares , 2):
            if sq1.has_overlap(sq2):
                if sq1 not in conflicts:
                    conflicts[sq1] = []
                if sq2 not in conflicts:
                    conflicts[sq2] = []
                    
                conflicts[sq1].append(sq2)
                conflicts[sq2].append(sq1)

        return conflicts
    
    def _phase_1(self, size):
        for point in self.points:
            point.squares = [Square(point, orientation, size) for orientation in ORIENTATIONS]

        for point1, point2 in itertools.combinations(self.points, 2):
            for square in point1.squares:
                if square.has_point(point2):
                    # TODO : don't creat an object here
                    sq = Square(point2, square.get_opposite_orientation(), size)
                    if sq in point2.squares:
                        point2.squares.remove(sq)
                    point1.squares.remove(square)

        square_list = []
        for point in self.points:
            square_list = square_list + point.squares

        return B.get_conflicts(square_list)


    def _phase_2(self, size):
        pass

    def _phase_3(self, size):
        pass

    def search(self, square_size):

        self._phase_2(square_size)
        self._phase_3(square_size)

        return self._phase_1(square_size)
        







# prekklapanja = {
#     tacka 1.1 : [tacakap1, tackap2,...]
#     tacka 1.2 : [tacakap1, tackap2,...]
# }



# def remove_sq_from_konf(konf,sq):
#     for sq1 in konf[sq]:
#         konf[sq1].remove(sq)
        