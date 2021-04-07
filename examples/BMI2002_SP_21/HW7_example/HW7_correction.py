import argparse

def solve(a, b, c, real_roots=True):
    print(a, b, c, real_roots)

parser = argparse.ArgumentParser(description='Example arg parsing that solves a mistake in HW 7')
parser.add_argument('a', type=float, help="coefficient 'a' in a quadratic equation")
parser.add_argument('b', type=float, help="coefficient 'b' in a quadratic equation")
parser.add_argument('c', type=float, help="coefficient 'c' in a quadratic equation")
parser.add_argument('--hide_complex_roots', action='store_false',
    help='if set, show complex roots of the quadratic equation; otherwise they raise errors')
args = parser.parse_args()

solve(args.a, args.b, args.c, real_roots=args.hide_complex_roots)
