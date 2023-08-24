import itertools
import random

from searches.optimal_search import OptimalSearch
from geometry.square import Square, ORIENTATIONS


class B(OptimalSearch):
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

        # for point1, point2 in itertools.combinations(self.points, 2):
        #     for square in point1.squares:
        #         if square.has_point(point2):
        #             # TODO : don't creat an object here
        #             sq = Square(point2, square.get_opposite_orientation(), size)
        #             if sq in point2.squares:
        #                 point2.squares.remove(sq)

        # for point1, point2 in itertools.combinations(self.points, 2):
        #     for square in point1.squares:
        #         if square.has_point(point2):
        #             point1.squares.remove(square)
        
        for point1 in self.points:
            for point2 in self.points:
                for square in point1.squares:
                    if square.has_point(point2):
                        if square in point1.squares:
                            point1.squares.remove(square)
        square_list = []
        for point in self.points:
            square_list = square_list + point.squares
        conflicts = B.get_conflicts(square_list)
        return conflicts, self.get_non_conflicts(conflicts)
    
    def remove_candidat(self, candidat, conflicts, non_conflicts):
        if candidat in conflicts:
            if conflicts[candidat]:
                for square in conflicts[candidat]:
                    conflicts[square].remove(candidat)
                    if not conflicts[square]:
                        del conflicts[square]
            del conflicts[candidat]
        if candidat.point in non_conflicts:
            if candidat in non_conflicts[candidat.point]:
                non_conflicts[candidat.point].remove(candidat)
            if not non_conflicts[candidat.point]:
                del non_conflicts[candidat.point]
        for point in self.points:
            if point == candidat.point:
                point.squares.remove(candidat)
                break
        return conflicts, non_conflicts
            
    def _phase_2(self, size):
        conflicts, non_conflicts = self._phase_1(size)
        stack = []
        for p in self.points:
            stack.append(p)
            stack_remove = []
            for point in stack:
                candidat_remove = []
                if len(point.squares) == 0:
                    return {}, {}
                elif point in non_conflicts:
                    if non_conflicts[point]:
                        chosen_square = random.choice(non_conflicts[point])
                        for square in point.squares:
                            if square != chosen_square:
                                candidat_remove.append(square)
                        non_conflicts[point] = [chosen_square]
                        stack_remove.append(point)
                elif len(point.squares) == 1:
                    if point.squares[0] in conflicts:
                        for square in conflicts[point.squares[0]]:
                            candidat_remove.append(square)
                        if point not in non_conflicts:
                            non_conflicts[point] = []
                        non_conflicts[point].append(point.squares[0])
                else:
                    for square in point.squares:
                        if square in conflicts:
                            for sq1, sq2 in itertools.combinations(conflicts[square], 2):
                                if sq1.point == sq2.point and len(sq1.point.squares) == 2:
                                    candidat_remove.append(square)
                                    break
                if candidat_remove:
                    for candidat in candidat_remove:
                        conflicts, non_conflicts = self.remove_candidat(candidat, conflicts, non_conflicts)
                    non_conflicts = self.get_non_conflicts(conflicts)
            if stack_remove:
                for remove in stack_remove:
                    stack.remove(remove)
        for point in self.points:
            if not point.squares:
                return {}, {}
        # print(f"----{size}---")
        # print(f"conflicts: {conflicts}")
        # print(f"non_conflicts: {non_conflicts}")
        # for point in self.points:
        #     print(f"    tacka {point} ima sledece kandidate: {point.squares}")
        # square_orientation = [point.squares[0] for point in self.points]
        return conflicts, non_conflicts

    def is_solution(self):
        for point in self.points:
            if not point.squares:
                return False
        return True
    
    def sat_combinations(self,conflicts, sat):
        print(conflicts)
        for sq1, sq2 in itertools.combinations(sat.keys(), 2):
            if sq1.point == sq2.point:
                sat[sq2] = not sat[sq1]
            if sq2 in conflicts[sq1]:
                if sat[sq1] == True:
                    sat[sq2] = False
        for candidat in conflicts:
            for square in conflicts[candidat]:
                if sat[candidat] == sat[square] == True:
                    print(f"sat_comb False: {candidat} {sat[candidat]} je isti kao {square} {sat[square]}")
                    return False
        for sq1, sq2 in itertools.combinations(sat.keys(), 2):
            if sq1.point == sq2.point:
                if sat[sq1] == sat[sq2] == False:
                    print(f"sat_comb False: {sq1} {sat[sq1]} i {sq2} {sat[sq2]}")
                    return False

    def two_sat(self, conflicts, non_conflicts):
        sat = {}
        for key in conflicts.keys():
            sat[key] = True
        if not self.sat_combinations(conflicts, sat):
            for key in sat.keys():
                sat[key] = False
        return self.sat_combinations(conflicts,sat)

    def _phase_3(self, size):
        print(f"----------{size}-------------")
        for i in range(0,3):
            conflicts, non_conflicts = self._phase_2(size)
            if (not non_conflicts) and (not conflicts):
                    return False
            for point in self.points:
                max_conf = 0
                max_sq = point.squares[0]
                if len(point.squares) == 4 - i:
                    for square in point.squares:
                        if square in conflicts:
                            if len(conflicts[square]) > max_conf:
                                max_conf = len(conflicts[square])
                                max_sq = square
                    conflicts, non_conflicts = self.remove_candidat(max_sq, conflicts, non_conflicts)
                    non_conflicts = self.get_non_conflicts(conflicts)

        for point in self.points:
            print(f"{point} ima {len(point.squares)} kandidata")
        sat_rez = True
        if conflicts:
            print(f"if conflicts : {conflicts}")
            return False
            # sat_rez =  self.two_sat(conflicts, non_conflicts)
            # print(f"faza3 sat vraca{sat_rez}")
        # if not sat_rez:
        #     return False
        
        if self.is_solution():
            return [point.squares[0] for point in self.points]
        else:
            return False


    def _search_size(self, square_size):
        return self._phase_3(square_size)
