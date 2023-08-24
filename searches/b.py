import itertools
import random

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

        for point1, point2 in itertools.combinations(self.points, 2):
            for square in point1.squares:
                if square.has_point(point2):
                    point1.squares.remove(square)
        
        # for point1 in self.points:
        #     for point2 in self.points:
        #         for square in point1.squares:
        #             if square.has_point(point2):
        #                 if square in point1.squares:
        #                     point1.squares.remove(square)

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
        stack_good = []
        # print(".................")
        # print(size)
        for i in range(0,2):
            for p in self.points:
                stack.append(p)
                # pop = False
                # print(f"{p}, num_sq: {len(p.squares)}, in_non_conflicts: {p in non_conflicts}, ")
                for point in stack:
                    if len(point.squares) == 0:
                        return False

                    elif point in non_conflicts:
                        if non_conflicts[point]:
                            chosen_square = random.choice(non_conflicts[point])
                            for square in point.squares:
                                if square != chosen_square:
                                    conflicts = B.remove_candidat(square, conflicts)
                                    # print(f"no_conflict :{point} , {square.orientation}")
                            stack.remove(point)
                            stack_good.append(chosen_square)

                    elif len(point.squares) == 1:
                        for square in conflicts[point.squares[0]]:
                            if square in stack_good:
                                return False
                            conflicts = B.remove_candidat(square, conflicts)
                        if point not in non_conflicts:
                            non_conflicts[point] = []
                        non_conflicts[point].append(point.squares[0])

                            # print(f"last_one: {square.point} , {square.orientation}")
                        # stack.remove(point)
                        # stack_good.append(square)

                    else:
                        for square in point.squares:
                            for sq1, sq2 in itertools.combinations(conflicts[square], 2):
                                if sq1.point == sq2.point and len(sq1.point.squares) == 2:
                                    B.remove_candidat(square, conflicts)
                                    # print(f"overlaps 2 finals: {square.point} , {square.orientation}")
                                    break
            # if pop:
            #     stack.pop()

        for point in self.points:
            if len(point.squares) == 0:
                return False
            if len(point.squares) > 1:
                hold = point.squares[0]
                for square in point.squares:   
                    B.remove_candidat(square, conflicts)
                    # print(f"after: {point} , {square.orientation}")
                point.squares.append(hold)
                # print(f"hold : {point} , {hold.orientation}")

        square_orientation = [point.squares[0] for point in self.points]

        return square_orientation

    def _phase_3(self, size):
        pass

    def _search_size(self, square_size):

        self._phase_3(square_size)

        return self._phase_2(square_size)
