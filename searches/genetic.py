from searches.search import Search

class Individual:
    def __init__(self, map) -> None:
        self.map = map
        self.fitness = 0
        self.calculate_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def calculate_fitness(self):
        pass

    def mutate(self):
        pass


class Genetic(Search):
    def __init__(
            self,
            map,
            iterations=1000,
            population_size=100,
            elitism_size=0.2,
            tournament_size=0.05,
            mutation_prob=0.02,
        ) -> None:
        super().__init__(map)

        self.iterations = iterations
        self.population_size = population_size
        self.elitism_size = int(population_size * elitism_size)
        self.tournament_size = int(population_size * tournament_size)
        self.mutation_prob = mutation_prob

    def _selection(self, population):
        return population[0] # TODO

    def _crossover(self, parent1, parent2, child1, child2):
        pass # TODO Maybe change this to static

    def search(self):
        population = [Individual(self.map) for _ in range(self.population_size)]
        new_population = [Individual(self.map) for _ in range(self.population_size)]

        for _ in range(self.iterations):
            population.sort() # TODO Maybe reverse

            new_population[:self.elitism_size] = population[:self.elitism_size]

            for i in range(self.elitism_size, self.population_size, 2):
                child1, child2 = new_population[i], new_population[i+1]
                parent1, parent2 = self._selection(population), self._selection(population)

                self._crossover(parent1, parent2, child1, child2)

                child1.mutate()
                child2.mutate()

                population = new_population # TODO Copy this

        return max(population) # TODO Return square placing
