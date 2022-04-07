import random


def generate_points(num_of_points, map_size, seed):
    random.seed(seed)
    points = set()
    for i in range(num_of_points):
        point = (random.uniform(0, map_size), random.uniform(0, map_size))
        if point in points:
            i -= 1
        else:
            points.add(point)

    return list(points)
