import random
from copy import deepcopy

from searches.search import Search
from geometry.square import ORIENTATIONS, ProtoSquare, Square

class Individual:
    def __init__(self, map, mutation_prob) -> None:
        self.map = map
        self.mutation_prob = mutation_prob

        self.sizes = map.square_size_candidates
        # self.size = self.sizes[0]
        self.size = random.choice(self.sizes)
        self.proto_squares = [ProtoSquare(p, random.choice(ORIENTATIONS)) for p in self.map.points]
        self.squares = []
        self._generate_squares()

        self.fitness = 0
        self._calculate_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def _generate_squares(self):
        self.squares = [Square.from_proto(psq, self.size) for psq in self.proto_squares]

    def _calculate_fitness(self):
        self.fitness = self.size
        if Square.check_overlap(self.squares):
            self.fitness *= -1

    def _mutate_size(self):
        if self.mutation_prob < random.random():
            return False

        size_index = self.sizes.index(self.size)

        if random.random() < 0.75:
            self.size = self.sizes[min(size_index, len(self.squares) - 1)]
        else:
            self.size = self.sizes[max(size_index - 1, 0)]

        return True

    def _mutate_squares(self):
        for i in range(len(self.proto_squares)):
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

    def __repr__(self) -> str:
        return str(self.fitness)


class Genetic(Search):
    def __init__(
            self,
            map,
            iterations=100,
            population_size=10,
            elitism_size=0.2,
            tournament_size=0.05,
            mutation_prob=0.02,
        ) -> None:
        super().__init__(map)

        self.iterations = iterations
        self.population_size = population_size
        self.elitism_size = max(int(population_size * elitism_size), 2)
        self.tournament_size = max(int(population_size * tournament_size), 2)
        self.mutation_prob = mutation_prob

    def _selection(self, population):
        return max(random.sample(population, self.tournament_size))

    def search(self):
        population = [Individual(self.map, self.mutation_prob) for _ in range(self.population_size)]
        new_population = [Individual(self.map, self.mutation_prob) for _ in range(self.population_size)]

        for _ in range(self.iterations):
            population.sort(reverse=True)
            new_population[:self.elitism_size] = deepcopy(population[:self.elitism_size])

            for i in range(self.elitism_size, self.population_size, 2):
                child1, child2 = new_population[i], new_population[i+1]
                parent1, parent2 = self._selection(population), self._selection(population)

                Individual.crossover(parent1, parent2, child1, child2)

                child1.mutate() # Maybe move to crossover, because of optimisation
                child2.mutate()

            population, new_population = new_population, population

        return max(population).squares
