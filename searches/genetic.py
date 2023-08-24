from searches.search import Search


class Genetic(Search):
    def __init__(self, map, iterations, population_size) -> None:
        super().__init__(map)
        self.iterations = iterations
        self.population_size = population_size

    def search(self):
        return super().search()
