class OptimalSearch:
    def __init__(self, map) -> None:
        self.map = map
        self.points = map.points

    def _search_size(self, square_size):
        """
        Args:
            squre_size - the size of square to search for

        Returns:
            False - if there is no solution for that size
            square_orientations - if there is a solution for this size

        """
        raise Exception("Not implemented.")

    def search(self):
        """
        Does a binary search through the maps square_size_candidates,
        and for each size check if there exist a viable placing.

        Returns:
            best_placing - list( Square )
        """
        squre_sizes = self.map.square_size_candidates

        l_bound = 0
        u_bound = len(squre_sizes) - 1

        best_placing = self._search_size(squre_sizes[u_bound])
        if best_placing:
            return best_placing

        best_placing = self._search_size(squre_sizes[l_bound])

        while True:
            m_bound = int((l_bound + u_bound) / 2)
            placing = self._search_size(squre_sizes[m_bound])
            if placing:
                best_placing = placing
                l_bound = m_bound
            else:
                u_bound = m_bound
            if u_bound - l_bound <= 1:
                break

        return best_placing
