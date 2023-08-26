import itertools
import random

import constraint

from searches.optimal_search import OptimalSearch
from geometry.square import Square, ORIENTATIONS


class B(OptimalSearch):
    def __init__(self, map) -> None:
        super().__init__(map)
        self.size = None
        self.conflicts = None
        self.non_conflicts = None

    def get_conflicts(self, squares):
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
        non_conflicts = dict()
        for point in self.points:
            for square in point.squares:
                if square not in self.conflicts:
                    if point not in non_conflicts:
                        non_conflicts[point] = []
                    non_conflicts[point].append(square)
        self.non_conflicts = non_conflicts

    def _phase_1(self):
        for point in self.points:
            point.squares = [Square(point, orientation, self.size) for orientation in ORIENTATIONS]        
        for point1 in self.points:
            for point2 in self.points:
                for square in point1.squares:
                    if square.has_point(point2):
                        if square in point1.squares:
                            point1.squares.remove(square)
        square_list = []
        for point in self.points:
            square_list = square_list + point.squares
        self.get_conflicts(square_list)
        self.get_non_conflicts()
    
    def remove_candidat(self, candidat):
        if candidat in self.conflicts:
            if self.conflicts[candidat]:
                for square in self.conflicts[candidat]:
                    self.conflicts[square].remove(candidat)
                    if not self.conflicts[square]:
                        del self.conflicts[square]
            del self.conflicts[candidat]
        if candidat.point in self.non_conflicts:
            if candidat in self.non_conflicts[candidat.point]:
                self.non_conflicts[candidat.point].remove(candidat)
            if not self.non_conflicts[candidat.point]:
                del self.non_conflicts[candidat.point]
        for point in self.points:
            if point == candidat.point:
                point.squares.remove(candidat)
                break
        self.get_non_conflicts()

    def posible(self):
        for point in self.points:
            if not point.squares:
                return False
        return True

    def _phase_2(self):
        stack = []
        for p in self.points:
            stack.append(p)
            stack_remove = []
            for point in stack:
                candidat_remove = []
                if len(point.squares) == 0:
                    return False
                elif point in self.non_conflicts:
                    if self.non_conflicts[point]:
                        chosen_square = random.choice(self.non_conflicts[point])
                        for square in point.squares:
                            if square != chosen_square:
                                candidat_remove.append(square)
                        self.non_conflicts[point] = [chosen_square]
                        stack_remove.append(point)
                elif len(point.squares) == 1:
                    if point.squares[0] in self.conflicts:
                        for square in self.conflicts[point.squares[0]]:
                            candidat_remove.append(square)
                        if point not in self.non_conflicts:
                            self.non_conflicts[point] = []
                        self.non_conflicts[point].append(point.squares[0])
                else:
                    for square in point.squares:
                        if square in self.conflicts:
                            for sq1, sq2 in itertools.combinations(self.conflicts[square], 2):
                                if sq1.point == sq2.point and len(sq1.point.squares) == 2:
                                    candidat_remove.append(square)
                                    break
                if candidat_remove:
                    for candidat in candidat_remove:
                        self.remove_candidat(candidat)
            if stack_remove:
                for remove in stack_remove:
                    stack.remove(remove)
        if not self.posible:
            return False
        return True

    def overlap(self, x, y):
        for key, value in x.items():
            x_sq = key
            x_t = value
        for key, value in y.items():
            y_sq = key
            y_t = value
        if x_t and y_t:
            if y_sq in self.conflicts[x_sq]:
                return False
        return True

    def count_true(solution):
        if solution:
            values = []
            for value in solution.values():
                if value.values():
                    tmp = list(value.values())
                    values = values + tmp 
            return sum(1 for value in values if value)
        else:
            return 0

    def solution_to_dict(solution):
        if solution:
            keys = []
            values = []
            for key in solution.values():
                keys = keys + list(key.keys())
            for value in solution.values():
                values = values + list(value.values())
            return dict(zip(keys, values))
        else: 
            return None

    def satisfiable(solution):
        points = set([square.point for square in solution.keys()])
        points_true = set([square.point for square, value in solution.items() if value])
        if points == points_true:
            return True
        else:
            return False

    def two_sat(self):
        if not self.conflicts:
            return True
        problem = constraint.Problem()
        str_conf = []
        for square in self.conflicts.keys():
            str_conf.append(str(square))
            problem.addVariable(str(square), [{square: True},{square: False}])
        for str1,str2 in itertools.combinations(str_conf,2):
            problem.addConstraint(self.overlap, (str1,str2))

        solutions = problem.getSolutions()
        if not solutions:
            return False    
        max_true = max(solutions, key=B.count_true)
        max_count = B.count_true(max_true)
        best_solutions = [solution for solution in solutions if B.count_true(solution) == max_count]
        finals = []
        for solution in best_solutions:
            finals.append(B.solution_to_dict(solution))
        for solution in finals:
            if B.satisfiable(solution):
                for key, value in solution.items():
                    if not value:
                        self.remove_candidat(key)
                return True
        return False

    def _phase_3(self):
        self._phase_1()
        for i in range(0,2):
            for point in self.points:
                max_conf = 0
                max_sq = point.squares[0]
                if len(point.squares) == 4 - i + 1:
                    for square in point.squares:
                        if square in self.conflicts:
                            if len(self.conflicts[square]) > max_conf:
                                max_conf = len(self.conflicts[square])
                                max_sq = square
                    self.remove_candidat(max_sq)
            if not self._phase_2():
                    return False
        if self.two_sat():
            if self.posible():
                return [point.squares[0] for point in self.points]
        return False


    def _search_size(self, square_size):
        self.size = square_size
        return self._phase_3()
