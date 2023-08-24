import itertools

from searches.optimal_search import OptimalSearch
from square import Square, ORIENTATIONS

class BruteForce(OptimalSearch):
    def _test_placings(self, square_orientations, square_size):
        """
        For the given square size, test if the given placings are valid.
        Args:
            square_size - size of the square (float)
            square_orientations - A list of sqaure orientations for each point
        Returns:
            boolean

        """
        squares = [Square(p, o, square_size) for (p, o) in zip(self.points, square_orientations)]

        for first, second in itertools.combinations(squares, 2):
            if first.has_overlap(second):
                return False
        return squares


    def _search_size(self, square_size):
        """
        A simple algorithm that goes through all the possible combinations
        of square orientations for the points and checks if they're valid.

        If one is valid returns the square placing combination, otherwise it returns False.
        """
        for square_placings in itertools.product(ORIENTATIONS, repeat=len(self.points)):
            if squares := self._test_placings(square_placings, square_size):
                return squares
        return False
