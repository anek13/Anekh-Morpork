#!/usr/bin/python3

import dungen
import random
import math
import itertools
import shutil
import argparse
import sys

parser = argparse.ArgumentParser(description='Demonstrate a shortest path algorithm on a randomly generated map.')
parser.add_argument('--seed', type=int, help='pseudo-random number generator seed')
parser.add_argument('--rows', type=int, help='number of rows')
parser.add_argument('--cols', type=int, help='number of columns')
args = parser.parse_args()

if args.seed:
	seed = args.seed
else:
	seed = random.randrange(sys.maxsize)
random.seed(seed)

if args.rows and args.cols:
	rows = args.rows
	cols = args.cols
else:
	term_size = shutil.get_terminal_size((80, 20))
	rows = term_size.lines - 2
	cols = term_size.columns

m = dungen.Map(cols, rows)
dungen.GoblinHalls(m)

empty_spaces = []
for y in range(m.height):
	for x in range(m.width):
		if m.get(x,y) == 1:
			empty_spaces.append((x,y))

def RandomEmptySpace(m):
	return random.choice(empty_spaces)

def distance(a,b):
	return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

pairs = [(RandomEmptySpace(m), RandomEmptySpace(m)) for i in range(100)]
distances = [distance(f,t) for (f,t) in pairs]
f,t = pairs[distances.index(max(distances))]

m.special[f] = '\033[41;37;1m' + 'F' + '\033[0m'
m.special[t] = '\033[41;37;1m' + 'T' + '\033[0m'

path = []

def sgn(x):
	if x > 0:
		return 1
	elif x < 0:
		return -1
	else:
		return 0

arrow_map = dict(zip(itertools.product([-1,0,1],[-1,0,1]), "↖←↙↑X↓↗→↘"))

i = f
while i != t:
	d = (sgn(t[0] - i[0]), sgn(t[1] - i[1]))
	i = (i[0] + d[0], i[1] + d[1])
	path.append(i)

last = None
for i in path:
	if last:
		m.special[last] = arrow_map[i[0] - last[0], i[1] - last[1]]
	last = i

print(m, end='')
print("{argv0} --seed={seed} --rows={rows} --cols={cols}".format(argv0=sys.argv[0], seed=seed, rows=rows, cols=cols))
