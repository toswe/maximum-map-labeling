import pickle
import os.path

from searches.brute_force import BruteForce

class BruteForceCache(BruteForce):
    """
    This search algorithm is the same as BruteForce,
    the only difference being it caches the search result.

    Because the BruteForce algorithm and map generation are deterministic,
    given the number of points, map size and the map seed the outcome will always be the same.
    """
    def _generate_cache_name(self):
        return (
            "cache/"
            f"points-{self.map.num_of_points}_"
            f"size-{self.map.size}_"
            f"seed-{self.map.seed}.pickle"
        )

    def _store_solution(self, best_placing):
        with open(self._generate_cache_name(), 'wb') as handle:
            pickle.dump(best_placing, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def _load_solution(self):
        with open(self._generate_cache_name(), 'rb') as handle:
            return pickle.load(handle)

    def _check_solution(self):
        return os.path.isfile(self._generate_cache_name())

    def search(self):
        if self._check_solution():
            return self._load_solution()

        best_placing = super().search()

        self._store_solution(best_placing)

        return best_placing
