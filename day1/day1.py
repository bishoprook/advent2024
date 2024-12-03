import argparse
import re

parser = argparse.ArgumentParser(prog='AOC2024-d01')
parser.add_argument('filename')
args = parser.parse_args()

# Reading the input data, which is in lines of number pairs.
pattern = r"(\d+)\s+(\d+)"
with open(args.filename, 'r') as file:
    matches = [re.search(pattern, line).groups() for line in file]

list_a = [int(a) for a, _ in matches]
list_a.sort()
list_b = [int(b) for _, b in matches]
list_b.sort()

distances = [abs(a - b) for a, b in zip(list_a, list_b)]
print("Total distance: ", sum(distances))

count_size = max(max(list_a), max(list_b)) + 1

counts_a = [0] * count_size
for value in list_a:
    counts_a[value] += 1

counts_b = [0] * count_size
for value in list_b:
    counts_b[value] += 1

products = [idx * counts_a[idx] * counts_b[idx] for idx in range(count_size)]
print("Result: ", sum(products))