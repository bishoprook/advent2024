import argparse
import re

parser = argparse.ArgumentParser(prog='AOC2024-01')
parser.add_argument('filename')
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

def logd(*input):
    if args.debug:
        print(*input)

pattern = r"(\d+)\s+(\d+)"
list_a = []
list_b = []
with open(args.filename, 'r') as file:
    for line in file:
        match = re.search(pattern, line)
        a, b = match.groups()
        list_a.append(int(a))
        list_b.append(int(b))
        logd("Input row: ", a, b)

list_a.sort()
list_b.sort()

distances = [abs(list_a[idx] - list_b[idx]) for idx in range(0, len(list_a))]

print("Distances: ", distances)

total_distance = sum(distances)

print("Total distance: ", total_distance)