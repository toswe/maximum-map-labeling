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
        self.proto_squares = [ProtoSquare(p, random.choice(ORIENTATIONS)) for p in self.map.points]

        self.fitness = self._calculate_fitness()        

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self) -> str:
        return str(self.fitness)
    
    def _generate_squares(self, size):
        return [Square.from_proto(sq, size) for sq in self.proto_squares]

    def _search_size(self, size):
        # TODO Implement a version that doesn't generate squares and optimizes search
        if Square.check_overlap(self._generate_squares(size)):
            return False
        return size

    def _calculate_fitness(self):
        l_bound = 0
        u_bound = len(self.sizes) - 1

        fitness = self._search_size(self.sizes[u_bound])
        if fitness:
            return fitness

        fitness = self._search_size(self.sizes[l_bound])

        while True:
            m_bound = int((l_bound + u_bound) / 2)
            placing = self._search_size(self.sizes[m_bound])
            if placing:
                fitness = placing
                l_bound = m_bound
            else:
                u_bound = m_bound
            if u_bound - l_bound <= 1:
                break

        return fitness

    def _should_mutate(self):
        return self.mutation_prob > random.random()

    def _mutate_proto_squares(self):
        for i in range(len(self.proto_squares)):
            if self._should_mutate():
                self.proto_squares[i].orientation = random.choice(ORIENTATIONS) # TODO Check if same orientation

    def _update_and_mutate(self, proto_squares):
        self.proto_squares = deepcopy(proto_squares)

        self._mutate_proto_squares()
        self.fitness = self._calculate_fitness()

    @staticmethod
    def crossover_1_position(parent1, parent2, child1, child2):
        split_index = random.randrange(len(parent1.proto_squares))

        proto_squares_1 = parent1.proto_squares[:split_index] + parent2.proto_squares[split_index:]
        proto_squares_2 = parent2.proto_squares[:split_index] + parent1.proto_squares[split_index:]

        child1._update_and_mutate(proto_squares_1)
        child2._update_and_mutate(proto_squares_2)

    @staticmethod
    def crossover_uniform(parent1, parent2, child1, child2):
        proto_squares_1, proto_squares_2 = zip(*[
            (first, second) if random.random() > 0.5 else (second, first)
            for first, second in zip(parent1.proto_squares, parent2.proto_squares)
        ])

        child1._update_and_mutate(proto_squares_1)
        child2._update_and_mutate(proto_squares_2)

    @staticmethod
    def crossover(parent1, parent2, child1, child2):
        # Individual.crossover_1_position(parent1, parent2, child1, child2)
        Individual.crossover_uniform(parent1, parent2, child1, child2)


class KarteljGenetic(Search):
    def __init__(
            self,
            map,
            iterations=20,
            population_size=100,
            elitism_size=0.2,
            tournament_size=5,
            mutation_prob=0.01,
        ) -> None:
        super().__init__(map)

        self.iterations = iterations
        self.population_size = int(population_size / 2) * 2
        self.elitism_size = int(population_size * elitism_size / 2) * 2
        self.tournament_size = min(population_size, tournament_size)
        self.mutation_prob = mutation_prob

    def _selection(self, population):
        return max(random.sample(population, self.tournament_size))

    def search(self):
        random.seed()

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

        return population[0]._generate_squares(population[0].fitness)
