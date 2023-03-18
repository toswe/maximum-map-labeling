import generate
import utils
import searches
import typer


app = typer.Typer()

"""
run: 
    python main.py --num_points 10 --map_size 100 --seed aNiceSeed 
    python main.py -n 10 -m 100 -s aNiceSeed   
"""

app.command()
def main(
        num_points: int = typer.Option('10', '--num_points', '-n', 
                                       help = "Number of points to be generated"),
        map_size: float = typer.Option('100', '--map_size', '-m', help = "Size of the squared map"),
        seed: str = typer.Option('aNiceSeed', '--seed', '-s', help = "Name of the seed")
) ->None:
    POINTS = generate.generate_points(num_points, map_size, seed)
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

if __name__ == "__main__":
    typer.run(main)