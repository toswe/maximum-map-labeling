import time

from geometry.map import Map
from searches.b import B
from searches.genetic import Genetic
from searches.improved_genetic import ImprovedGenetic

MAP_SIZE = 100
NUM_OF_SEEDS = 10
NUM_OF_POINTS = [
    5,
    10,
    20,
    100,
    200,
    1000,
    2000,
    10000,
]
SEARCH_ALGORITHMS = [
    # B,
    # Genetic,
    ImprovedGenetic,
]


def write_header(file_name):
    with open(file_name, "w") as file:
        search_headers = [f'{sa.__name__} size,{sa.__name__} elapsed' for sa in SEARCH_ALGORITHMS]
        header = f"number of points,seed,{','.join(search_headers)}\n"
        file.write(header)


def write_cell(file_name, cell):
    with open(file_name, "a") as file:
        file.write(f"{cell},")


def write_new_line(file_name):
    with open(file_name, "a") as file:
        file.write(f"\n")


def main():
    file_name = f'results/{time.time()}.csv'
    write_header(file_name)

    for num_of_points in NUM_OF_POINTS:
        for seed in range(NUM_OF_SEEDS):
            write_cell(file_name, f'{num_of_points},{seed}')
            print('#####################################################')
            print(f"Running for {num_of_points} points on seed {seed}.")
            print()

            the_map = Map(num_of_points, MAP_SIZE, seed)

            for algorithm in SEARCH_ALGORITHMS:
                print(f'Starting {algorithm.__name__} algorithm.')

                search = algorithm(the_map)
                squares, elapsed = search.search_with_time_measure()
                size = squares[0].size

                write_cell(file_name, f'{size},{elapsed}')
                print('Finnished in {:.2f}s with size: {:.2f}'.format(elapsed, size))
                print()

            write_new_line(file_name)


if __name__ == "__main__":
    main()
