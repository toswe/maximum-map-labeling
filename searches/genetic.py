import random
from copy import deepcopy

from searches.search import Search
from geometry.square import ORIENTATIONS, ProtoSquare, Square

class Individual:
    def __init__(self, map, mutation_prob) -> None:
        self.map = map
        self.mutation_prob = mutation_prob

        self.sizes = map.square_size_candidates
        self.size = random.choice(self.sizes)
        self.proto_squares = [ProtoSquare(p, random.choice(ORIENTATIONS)) for p in self.map.points]
        self.squares = []
        self._generate_squares()

        self.fitness = 0
        self._calculate_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def _generate_squares(self):
        self.squares = [Square(psq, self.size) for psq in self.proto_squares]

    def _calculate_fitness(self):
        if Square.check_overlap(self.squares):
            return 0
        return self.size

    def _mutate_size(self):
        if self.mutation_prob < random.random():
            return False

        size_index = self.sizes.index(self.size)

        if random.random() < 0.5:
            self.size = self.squares[min(size_index + 1, len(self.squares) - 1)]
        else:
            self.size = self.squares[max(size_index - 1, 0)]

        return True

    def _mutate_squares(self):
        for i in range(self.proto_squares):
            if random.random() < self.mutation_prob:
                self.proto_squares[i].orientation = random.choice(ORIENTATIONS) # TODO Check if same orientation
                self.squares[i] = Square.from_proto(self.proto_squares[i], self.size)

    def mutate(self):
        self._mutate_squares()
        if self._mutate_size():
            self._generate_squares()

        self._calculate_fitness()

    def _update(self, proto_squares, size):
        self.proto_squares = deepcopy(proto_squares)
        self.size = size
        self._generate_squares()
        self._calculate_fitness()

    @staticmethod
    def crossover(parent1, parent2, child1, child2):
        split_index = random.randrange(len(parent1.proto_squares))

        proto_squares_1 = parent1.proto_squares[:split_index] + parent2.proto_squares[split_index:]
        proto_squares_2 = parent2.proto_squares[:split_index] + parent1.proto_squares[split_index:]

        child1._update(proto_squares_1, parent1.size)
        child2._update(proto_squares_2, parent2.size)


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

    def search(self):
        population = [Individual(self.map) for _ in range(self.population_size)]
        new_population = [Individual(self.map) for _ in range(self.population_size)]

        for _ in range(self.iterations):
            population.sort() # TODO Maybe reverse

            new_population[:self.elitism_size] = population[:self.elitism_size]

            for i in range(self.elitism_size, self.population_size, 2):
                child1, child2 = new_population[i], new_population[i+1]
                parent1, parent2 = self._selection(population), self._selection(population)

                Individual.crossover(parent1, parent2, child1, child2)

                child1.mutate()
                child2.mutate()

            population = new_population # TODO Copy this

        return max(population).squares
