import itertools
import random

import constraint

from searches.optimal_search import OptimalSearch
from geometry.square import Square, ORIENTATIONS


class B(OptimalSearch):
    """
    This search algorithm checks if there is a solution for square placing for the given size and returns it.
    The algorithm is based on the research of Frank Wagner and Alexander Wolf:
    'An Efficient and Effective Approximation Algorithm for the Map Labeling Problem'.
    """
    def __init__(self, map) -> None:
        super().__init__(map)
        self.size = None
        self.conflicts = None
        self.non_conflicts = None

    def get_conflicts(self, squares):
        """
        Afunction that initiates dictionary of conflicts from list of squares.
        Args:
            squares: list of squares ([Square])
        """
        conflicts = dict()
        for sq1, sq2  in itertools.combinations(squares , 2):
            if sq1.has_overlap(sq2):
                if sq1 not in conflicts:
                    conflicts[sq1] = []
                if sq2 not in conflicts:
                    conflicts[sq2] = []
                conflicts[sq1].append(sq2)
                conflicts[sq2].append(sq1)
        self.conflicts = conflicts
    
    def get_non_conflicts(self):
        """
        A function that initiates dictionary of non-conflicts.
        """
        non_conflicts = dict()
        for point in self.points:
            for square in point.squares:
                if square not in self.conflicts:
                    if point not in non_conflicts:
                        non_conflicts[point] = []
                    non_conflicts[point].append(square)
        self.non_conflicts = non_conflicts

    def _phase_1(self):
        """
        A function that generates squares for every point,
        removes squares that overlap a point and
        initiates dictionaries of conflicts and non-conflicts.
        """
        for point in self.points:
            point.squares = [Square(point, orientation, self.size) for orientation in ORIENTATIONS]
        for point1, point2 in itertools.permutations(self.points,2):
            for square in point1.squares:
                if square.has_point(point2):
                    point1.squares.remove(square)
        square_list = []
        for point in self.points:
            square_list = square_list + point.squares
        self.get_conflicts(square_list)
        self.get_non_conflicts()
    
    def remove_candidat(self, candidat):
        """
        A function That removes square candidat from conflicts and point squares
        and regenerates non-conflicts.
        Args:
            candidat: square candidat to be removed (Square)
        """
        if candidat in self.conflicts:
            for square in self.conflicts[candidat]:
                self.conflicts[square].remove(candidat)
                if not self.conflicts[square]:
                    del self.conflicts[square]
            del self.conflicts[candidat]
        for point in self.points:
            if point == candidat.point:
                point.squares.remove(candidat)
                break
        self.get_non_conflicts()

    def is_possible(self):
        """
        A function that returns False if any point has no assigned squares, else True
        """
        for point in self.points:
            if not point.squares:
                return False
        return True

    def non_conflict_point(self,point):
        candidat_remove = []
        chosen_square = random.choice(self.non_conflicts[point])
        for square in point.squares:
            if square != chosen_square:
                candidat_remove.append(square)
        return candidat_remove

    def last_square(self,point):
        candidats_remove = []
        if point.squares[0] in self.conflicts:
            for square in self.conflicts[point.squares[0]]:
                candidats_remove.append(square)
        return candidats_remove

    def overlap_last_two(self,point):
        candidats_remove = []
        for square in point.squares:
            if square in self.conflicts:
                for sq1, sq2 in itertools.combinations(self.conflicts[square], 2):
                    if sq1.point == sq2.point and len(sq1.point.squares) == 2:
                        candidats_remove.append(square)
                        break
        return candidats_remove

    def _phase_2(self):
        """
        A function that goes through all the points and updates points and squares based on the following criteria:
            -Returns False if the point doesn't have a single candidate,
            -If point has non-conflit square, chooses a random candidate from the given point that
                is not in conflict and deletes all the others,
            -If it's the last square of the given point, it deletes all those it conflicts with,
            -It deletes all candidates of the point that overlap with the last two squares of some other point
        Returns:
            True - if solution is possible
            False - if solution is not possible
        """
        stack = []
        for p in self.points:
            stack.append(p)
            stack_remove = []
            for point in stack:
                candidats_remove = []

                if len(point.squares) == 0:
                    return False

                elif point in self.non_conflicts:
                    candidats_remove += self.non_conflict_point(point)
                    stack_remove.append(point)

                elif len(point.squares) == 1:
                    candidats_remove += self.last_square(point)

                else:
                    candidats_remove += self.overlap_last_two(point)

                if candidats_remove:
                    for candidat in candidats_remove:
                        self.remove_candidat(candidat)
            if stack_remove:
                for point in stack_remove:
                    stack.remove(point)
        if not self.is_possible():
            return False
        return True

    def two_sat(self):
        points = set([square.point for square in self.conflicts])
        cnf = constraint.Problem()

        if not points:
            return True
        
        for point in points:
            cnf.addVariable(point,[True,False])

        for p1,p2 in itertools.combinations(points,2):
            if len(p1.squares) == 1 and len(p2.squares) == 1:
                if p2.squares[0] in self.conflicts[p1.squares[0]]:
                    return False
                cnf.addConstraint(lambda p1, p2: (p1 and p2), (p1, p2))
            elif len(p1.squares) == 1:
                if p2.squares[0] in self.conflicts[p1.squares[0]]:
                    cnf.addConstraint(lambda p1, p2: p1 and (not p2), (p1, p2))
                if p2.squares[1] in self.conflicts[p1.squares[0]]:
                    cnf.addConstraint(lambda p1, p2: p1 and p2, (p1, p2))
            elif len(p2.squares) == 1:
                if p2.squares[0] in self.conflicts[p1.squares[0]]:
                    cnf.addConstraint(lambda p1, p2: (not p1) and p2, (p1, p2))
                if p2.squares[0] in self.conflicts[p1.squares[1]]:
                    cnf.addConstraint(lambda p1, p2: p1 and p2,(p1,p2))
            else:
                if p2.squares[0] in self.conflicts[p1.squares[0]]:
                    cnf.addConstraint(lambda p1, p2: not(p1 and p2), (p1, p2))
                if p2.squares[1] in self.conflicts[p1.squares[0]]:
                    cnf.addConstraint(lambda p1, p2: not(p1 and (not p2)), (p1, p2))
                if p2.squares[0] in self.conflicts[p1.squares[1]]:
                    cnf.addConstraint(lambda p1, p2: not((not p1) and p2),(p1,p2))
                if p2.squares[1] in self.conflicts[p1.squares[1]]:
                    cnf.addConstraint(lambda p1, p2: not((not p1) and (not p2)), (p1, p2))

        solution = cnf.getSolution()
        if not solution:
            return False
        for key, value in solution.items():
            if value:
                if len(key.squares) == 1:
                    continue
                self.remove_candidat(key.squares[1])
            else:
                self.remove_candidat(key.squares[0])
        return True

    def limit_squares(self, i):
        """
        A function that removes one square from points with i number of squares with the most conflicts
        Args:
            i - required number of squares
        Returns:
            False - if point has no squares
            True - if squares are successfully removed
        """
        for point in self.points:
            if len(point.squares) == i:
                max_conf = 0
                max_sq = point.squares[0]
                for square in point.squares:
                    if square in self.conflicts and len(self.conflicts[square]) > max_conf:
                        max_conf = len(self.conflicts[square])
                        max_sq = square
                self.remove_candidat(max_sq)


    def _phase_3(self):
        """
        A function that checks whether there is square placing for the given square size and returns it.
        It initiates squares for given size (phase one), removes squares with the most conflicts,
        checks for solution (phase two), then again removes squares with the most conflicts, than checks again for solution,
        and then does the final check (two sat).
        Returns:
            False - if the placing isn't possible
            list( Square ) - if the placing is found
        """
        self.limit_squares(4)
        if not self._phase_2():
            return False
        self.limit_squares(3)
        if not self._phase_2():
            return False
        if self.two_sat():
            if self.is_possible():
                return [point.squares[0] for point in self.points]
        return False

    def _search_size(self, square_size):
        self.size = square_size
        self._phase_1()
        return self._phase_3()
