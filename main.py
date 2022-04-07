import generate
import utils
import searches

NUM_OF_POINTS = 10
MAP_SIZE = 100
SEED = 'aNiceSeed'


def test_placing(points, square_size):
    return searches.moj_src(points, square_size)


def binary_search(points, limits):
    l_bound = 0
    u_bound = len(limits) - 1
    best_placing = test_placing(points, limits[u_bound])
    if best_placing:
        return u_bound, list(zip(points, best_placing))
    best_placing = test_placing(points, limits[l_bound])
    while True:
        print(l_bound, u_bound)
        m_bound = int((l_bound + u_bound) / 2)
        placing = test_placing(points, limits[m_bound])
        if placing:
            best_placing = placing
            l_bound = m_bound
        else:
            u_bound = m_bound
        if u_bound - l_bound <= 1:
            break
    return l_bound, list(zip(points, best_placing))


POINTS = generate.generate_points(NUM_OF_POINTS, MAP_SIZE, SEED)
print('Generated points:', POINTS)

LIMITS = utils.get_possible_square_sizes(utils.get_point_limits(POINTS))
print('Possible limits:', len(LIMITS), LIMITS)

opt_bound, opt_placings = binary_search(POINTS, LIMITS)

print(LIMITS[opt_bound], opt_placings)

