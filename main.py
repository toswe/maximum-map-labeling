import generate
import utils
import searches

NUM_OF_POINTS = 10
MAP_SIZE = 100
SEED = 'aNiceSeed'


POINTS = generate.generate_points(NUM_OF_POINTS, MAP_SIZE, SEED)
print('Generated points:', POINTS)

# If there exists a square size and placment in which no squares
# touch each other, that square size cannot be optimal since
# we can get a better result by increasing the square size
# until some two squares touch each other.
# Thus there are a limited number of possible square sizes
# that can possibly be optimal.
SQUARE_SIZE_CANDIDATES = utils.get_possible_square_sizes(
    utils.get_point_limits(POINTS)
)
print('Possible square size candidates:')
print(len(SQUARE_SIZE_CANDIDATES), SQUARE_SIZE_CANDIDATES)
print()

# We can then do a binary search through those
# possible square sizes and find the largest one which
# has a square placing that is valid.
opt_bound, opt_placings = utils.binary_search(
    SQUARE_SIZE_CANDIDATES, POINTS, searches.brute_force)

# opt_bound, opt_placings = binary_search(POINTS, SQUARE_SIZE_CANDIDATES, searches.moj_src)

print('The largest area of the squares:')
print((opt_bound ** 2) * len(POINTS))
print()
print("Optimal square size and placings:")
print(opt_bound, opt_placings)
