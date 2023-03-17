import typer

#typer.Option(default_value, name, short_name, help = description)

OPTION_NUM_POINTS = typer.Option('10', '--num_points', '-n', 
                                 help = "Number of points to be generated")
OPTION_MAP_SIZE = typer.Option('100', '--map_size', '-m', help = "Size of the squared map")
OPTION_SEED = typer.Option('aNiceSeed', '--seed', '-s', help = "Name of the seed")