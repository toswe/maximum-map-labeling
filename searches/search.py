import time


class Search:
    def __init__(self, map) -> None:
        self.map = map
        self.points = map.points

    def search(self):
        """
        Returns:
            best_placing - list( Square )
        """
        raise Exception("Not implemented.")

    def search_with_time_measure(self):
        start_time = time.time()
        result = self.search()
        elapsed = time.time() - start_time
        return result, elapsed
