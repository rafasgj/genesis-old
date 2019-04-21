"""Process CLI options."""

import argparse


def proccess_CLI():
    """Process Genesis command line options."""
    parser = argparse.ArgumentParser(description="Genesis")
    parser.add_argument('--version', action='version', version='%(prog)s 0.2')
    parser.add_argument("-m", "--mute", action='store_true', dest='mute',
                        help='Mute sound.')
    parser.add_argument("-w", "--windowed", dest='windowed',
                        action='store_true', help='Run in windowed mode.')
    msg = 'Use the given dimension instead of the highest one.'
    parser.add_argument("-s", "--size", action='store', dest="dimension",
                        metavar="DIM", nargs=2, type=int, help=msg)

    return parser.parse_args()
