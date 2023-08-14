class Search:
    def __init__(self, points) -> None:
        self.points = points

    def search(self, square_size):
        """
        Args:
            squre_size - the size of square to search for

        Returns:
            False - if there is no solution for that size
            square_orientations - if there is a solution for this size

        """
        raise Exception("Not implemented.")

    def binary_search(self, squre_sizes):
        """
        Args:
            squre_sizes - a list of possible sqare sizes (list(float))

        Returns:
            optimal_square_size - float
            points_and_their_orientation - list( ((float, float), int) )

        """
        l_bound = 0
        u_bound = len(squre_sizes) - 1

        best_placing = self.search(squre_sizes[u_bound])
        if best_placing:
            return squre_sizes[u_bound], list(zip(self.points, best_placing))

        best_placing = self.search(squre_sizes[l_bound])

        while True:
            m_bound = int((l_bound + u_bound) / 2)
            placing = self.search(squre_sizes[m_bound])
            if placing:
                best_placing = placing
                l_bound = m_bound
            else:
                u_bound = m_bound
            if u_bound - l_bound <= 1:
                break

        optimal_square_size = squre_sizes[l_bound]
        points_and_their_orientation = list(zip(self.points, best_placing))

        return optimal_square_size, points_and_their_orientation
