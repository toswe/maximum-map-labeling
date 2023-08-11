import itertools
from random import random

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
    
    def get_non_conflicts(self, conflicts):
        non_conflicts = dict()
        for point in self.points:
            for square in point.squares:
                if square not in conflicts:
                    if point not in non_conflicts:
                        non_conflicts[point] = []
                    non_conflicts[point].append(square)
        return non_conflicts
    
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

        conflicts = B.get_conflicts(square_list)
        return conflicts, self.get_non_conflicts(conflicts)
    
    def remove_candidat(candidat, conflicts):
        if candidat in conflicts:
            for square in conflicts[candidat]:
                conflicts[square].remove(candidat)
            del conflicts[candidat]

        candidat.point.squares.remove(candidat)

        return conflicts
            
    def _phase_2(self, size):
        conflicts, non_conflicts = self._phase_1(size)
        stack = []

        for p in self.points:
            stack.append(p)
            pop = True

            for point in stack:
                if len(point.squares) == 0:
                    return f"There is no solution for squares of size {size}"

                elif point in non_conflicts:
                    if non_conflicts[point]:
                        chosen_square = random.choice(non_conflicts[point])
                        for square in point.squares:
                            if square != chosen_square:
                                conflicts = B.remove_candidat(square, conflicts)
                        if point not in stack[:-1]:
                            pop = False

                elif len(point.squares) == 1:
                    for square in conflicts[point.squares[0]]:
                        conflicts = B.remove_candidat(square, conflicts)
                    if point not in stack[:-1]:
                        pop = False

                else:
                    for square in point.squares:
                        for sq1, sq2 in itertools.combinations(conflicts[square], 2):
                            if sq1.point == sq2.point:
                                B.remove_candidat(square, conflicts)
                                break
                if pop:
                    stack.pop()

        return conflicts

    def _phase_3(self, size):
        pass

    def search(self, square_size):

        self._phase_3(square_size)

        return self._phase_2(square_size)
