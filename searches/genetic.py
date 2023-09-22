import random
from copy import deepcopy

import itertools
import matplotlib.pyplot as plt

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

        self.max_overlaps = 3 # TODO Extract this
        self.fitness = 0
        self.has_overlaps = False
        self._calculate_fitness()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self) -> str:
        return str(self.fitness)

    def _generate_squares(self):
        self.squares = [Square.from_proto(psq, self.size) for psq in self.proto_squares]

    def _calculate_fitness_simple(self):
        self.fitness = self.size
        if Square.check_overlap(self.squares):
            self.fitness *= -1

    def _calculate_fitness_simple_with_overlaps(self):
        self.has_overlaps = False
        overlaps = 0

        for first, second in itertools.combinations(self.squares, 2):
            if first.has_overlap(second):
                self.has_overlaps = True
                overlaps += 1

            if overlaps > self.max_overlaps:
                self.fitness = -1 * self.size
                return

        self.fitness = self.size * (len(self.squares) - overlaps * 2)

    def _calculate_fitness_bidirectional(self):
        self.fitness = Square.get_no_overlap_length(self.squares)
        self.fitness += Square.get_no_overlap_length(reversed(self.squares))
        self.fitness *= self.size

    def _calculate_fitness(self):
        # self._calculate_fitness_simple()
        # self._calculate_fitness_simple_with_overlaps()
        self._calculate_fitness_bidirectional()

    def _should_mutate(self):
        return self.mutation_prob > random.random()

    def _grow_size(self):
        size_index = self.sizes.index(self.size)
        self.size = self.sizes[min(size_index + 1, len(self.squares) - 1)]

    def _shrink_size(self):
        size_index = self.sizes.index(self.size)
        self.size = self.sizes[max(size_index - 1, 0)]

    def _mutate_size(self):
        if not self._should_mutate():
            return

        if random.random() < 0.75:
            self._grow_size()
        else:
            self._shrink_size()

    def _mutate_proto_squares(self):
        for i in range(len(self.proto_squares)):
            if self._should_mutate():
                self.proto_squares[i].orientation = random.choice(ORIENTATIONS) # TODO Check if same orientation

    def _update_and_mutate(self, proto_squares, size):
        self.proto_squares = deepcopy(proto_squares)
        self.size = size

        self._mutate_proto_squares()
        self._mutate_size()
        self._generate_squares()

        self._calculate_fitness()

    @staticmethod
    def crossover_1_position(parent1, parent2, child1, child2):
        split_index = random.randrange(len(parent1.proto_squares))

        proto_squares_1 = parent1.proto_squares[:split_index] + parent2.proto_squares[split_index:]
        proto_squares_2 = parent2.proto_squares[:split_index] + parent1.proto_squares[split_index:]

        child1._update_and_mutate(proto_squares_1, parent1.size)
        child2._update_and_mutate(proto_squares_2, parent2.size)

    @staticmethod
    def crossover_uniform(parent1, parent2, child1, child2):
        proto_squares_1, proto_squares_2 = zip(*[
            (first, second) if random.random() > 0.5 else (second, first)
            for first, second in zip(parent1.proto_squares, parent2.proto_squares)
        ])

        size_1, size_2 = (
            (parent1.size, parent2.size)
            if random.random() > 0.5 else
            (parent2.size, parent1.size)
        )

        child1._update_and_mutate(proto_squares_1, size_1)
        child2._update_and_mutate(proto_squares_2, size_2)

    @staticmethod
    def crossover(parent1, parent2, child1, child2):
        Individual.crossover_1_position(parent1, parent2, child1, child2)
        # Individual.crossover_uniform(parent1, parent2, child1, child2)


class Genetic(Search):
    def __init__(
            self,
            map,
            iterations=10,
            population_size=100,
            elitism_size=0.2,
            tournament_size=5,
            mutation_prob=0.01,
        ) -> None:
        super().__init__(map)

        self.iterations = iterations
        self.population_size = int(population_size / 2) * 2
        self.elitism_size = max(int(population_size * elitism_size), 2)
        self.tournament_size = min(population_size, tournament_size)
        self.mutation_prob = mutation_prob

    def _selection(self, population):
        return max(random.sample(population, self.tournament_size))

    def search(self):
        population = [Individual(self.map, self.mutation_prob) for _ in range(self.population_size)]
        new_population = [Individual(self.map, self.mutation_prob) for _ in range(self.population_size)]

        fitnesses = []
        for _ in range(self.iterations):
            population.sort(reverse=True)
            fitnesses.append(population[0].fitness)

            new_population[:self.elitism_size] = deepcopy(population[:self.elitism_size])

            for i in range(self.elitism_size, self.population_size, 2):
                child1, child2 = new_population[i], new_population[i+1]
                parent1, parent2 = self._selection(population), self._selection(population)

                Individual.crossover(parent1, parent2, child1, child2)

            population, new_population = new_population, population

        # subplot = plt.figure().add_subplot()
        # subplot.plot(fitnesses)

        return max(p for p in population if not p.has_overlaps).squares
