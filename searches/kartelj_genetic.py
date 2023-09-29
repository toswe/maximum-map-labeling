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
        self.orientations = [random.choice(ORIENTATIONS) for _ in map.points]

        self.points = map.points
        self.close_points = map.close_points
        self.fitness = self._calculate_fitness()        

    def __lt__(self, other):
        return self.fitness < other.fitness

    def __repr__(self) -> str:
        return str(self.fitness)
    
    def _generate_squares(self, size):
        return [
            Square(p, o, size)
            for p, o in zip(self.points, self.orientations)
        ]

    def _search_size(self, size):
        for first_index, indexes in self.close_points.items():
            # TODO Implement a helper method insted of creating squares
            first = Square(self.points[first_index], self.orientations[first_index], size)

            for second_index in indexes:
                second = Square(self.points[second_index], self.orientations[second_index], size)
                if first.has_overlap(second):
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

    def _mutate(self):
        for i in range(len(self.orientations)):
            if self._should_mutate():
                self.orientations[i] = random.choice(ORIENTATIONS)

    def _update_and_mutate(self, orientations):
        self.orientations = orientations.copy()

        self._mutate()
        self.fitness = self._calculate_fitness()

    @staticmethod
    def crossover_1_position(parent1, parent2, child1, child2):
        split_index = random.randrange(len(parent1.orientations))

        orientations_1 = parent1.orientations[:split_index] + parent2.orientations[split_index:]
        orientations_2 = parent2.orientations[:split_index] + parent1.orientations[split_index:]

        child1._update_and_mutate(orientations_1)
        child2._update_and_mutate(orientations_2)

    @staticmethod
    def crossover_uniform(parent1, parent2, child1, child2):
        orientations_1, orientations_2 = zip(*[
            (first, second) if random.random() > 0.5 else (second, first)
            for first, second in zip(parent1.orientations, parent2.orientations)
        ])

        child1._update_and_mutate(list(orientations_1))
        child2._update_and_mutate(list(orientations_2))

    @staticmethod
    def crossover(parent1, parent2, child1, child2):
        # Individual.crossover_1_position(parent1, parent2, child1, child2)
        Individual.crossover_uniform(parent1, parent2, child1, child2)


class KarteljGenetic(Search):
    def __init__(
            self,
            map,
            iterations=50,
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
