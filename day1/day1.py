def load_lists(filename: str) -> tuple[list[int], list[int]]:
    """Load two lists from an input file and sort them. The input data is rows
    of two columns of numbers which are not sorted.
    
    :param str filename: the file to open
    :returns tuple[list[int], list[int]]: the two sorted lists"""
    import re
    pattern = r"(\d+)\s+(\d+)"
    with open(filename, 'r') as file:
        matches = [re.search(pattern, line).groups() for line in file]
        list_a = [int(a) for a, _ in matches]
        list_a.sort()
        list_b = [int(b) for _, b in matches]
        list_b.sort()
        return (list_a, list_b)

def total_distance(list_a: list[int], list_b: list[int]) -> int:
    """Find the total distance between two lists. For each index, the distance
    is defined as the difference between the values at that index. The total
    distance is the sum of distances at each index.

    :param list[int] list_a: the first input list
    :param list[int] list_b: the second input list
    :returns int: the total distance between the lists
    """
    distances = [abs(a - b) for a, b in zip(list_a, list_b)]
    return sum(distances)

def similarity(list_a: list[int], list_b: list[int]) -> int:
    """Find the similarity between two lists. For each value in list_a, the
    distance is defined as the product of the value and the number of times the
    same value appears in list_b. The similarity is the sum of the distances
    for each value in list_a. (Duplicates are allowed and will add to the
    similarity.)
    
    :param list[int] list_a: the first input list
    :param list[int] list_b: the second input list
    :returns int: the similarity between the two lists"""
    from itertools import groupby
    counts_b = { k: len(list(v)) for k, v in groupby(list_b) }
    products = [value * counts_b.get(value, 0) for value in list_a]
    return sum(products)

# Only try to load command-line arguments if we're in non-interactive mode. If
# imported into a REPL, we just want to test out the functions above.
import sys
interactive = hasattr(sys, 'ps1')
if not interactive:
    import argparse

    # Parse the command line arguments.
    parser = argparse.ArgumentParser(prog='AOC2024-d01')
    parser.add_argument('filename')
    args = parser.parse_args()

    list_a, list_b = load_lists(args.filename)

    print("Total distance: ", total_distance(list_a, list_b))
    print("Similarity: ", similarity(list_a, list_b))
