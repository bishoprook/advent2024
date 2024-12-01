import argparse
import re

parser = argparse.ArgumentParser(prog='AOC2024-d01')
parser.add_argument('filename')
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

def logd(*input):
    if args.debug:
        print(*input)

# Reading the input data, which is in lines of number pairs.
pattern = r"(\d+)\s+(\d+)"
with open(args.filename, 'r') as file:
    matches = [re.search(pattern, line).groups() for line in file]

list_a = [int(a) for a, _ in matches]
list_b = [int(b) for _, b in matches]

list_a.sort()
list_b.sort()

logd("List a: ", list_a)
logd("List b: ", list_b)

distances = [abs(a - b) for a, b in zip(list_a, list_b)]

logd("Distances: ", distances)

total_distance = sum(distances)

print("Total distance: ", total_distance)

count_size = max(max(list_a), max(list_b)) + 1
logd("Count size: ", count_size)

counts_a = [0] * count_size
counts_b = [0] * count_size

for value in list_a:
    counts_a[value] += 1
for value in list_b:
    counts_b[value] += 1

logd("Counts_a: ", counts_a)
logd("Counts_b: ", counts_b)

products = [idx * counts_a[idx] * counts_b[idx] for idx in range(0, count_size)]

logd("Products: ", products)

sum_products = sum(products)

print("Result: ", sum_products)