from typing import Generator, Literal, NewType, Self
from itertools import takewhile, pairwise
from more_itertools import unique

def logd(*_):
    pass

PageNum = NewType('PageNum', int)

class AdjacencyMatrix(object):
    def __init__(self, pages: list[PageNum], rules: list[tuple[PageNum, PageNum]]):
        self.pages = list(unique(pages))
        self.page_idx = { page: i for i, page in enumerate(self.pages) }
        width = len(self.pages)
        self.matrix = [[0] * (width) for _ in range(width)]
        for page_from, page_to in rules:
            self.set_adjacent(page_from, page_to)
    
    def has_page(self: Self, page: PageNum) -> bool:
        return self.page_idx.get(page) is not None

    def set_adjacent(self: Self, page_from: PageNum, page_to: PageNum) -> None:
        if not self.has_page(page_from) or not self.has_page(page_to):
            return
        idx_from, idx_to = self.page_idx[page_from], self.page_idx[page_to]
        self.matrix[idx_from][idx_to] = 1
        self.matrix[idx_to][idx_from] = -1

    def adjacencies(self: Self, page_from: PageNum, *pages_to: list[PageNum]) -> list[Literal[-1, 0, 1]]:
        idx_from = self.page_idx[page_from]
        return [self.matrix[idx_from][self.page_idx[page_to]] for page_to in pages_to]

    def __str__(self):
        header = '   ' + ' '.join(f"{page:2d}" for page in self.pages)
        rows = [f"{page:2d} " + ' '.join(f"{col:2d}" for col in row) for page, row in zip(self.pages, self.matrix)]
        return '\n'.join([header] + rows)

def valid(rules: list[tuple[PageNum, PageNum]], page_set: list[PageNum]) -> bool:
    matrix = AdjacencyMatrix(page_set, rules)
    adjacencies = [matrix.adjacencies(a, b)[0] for a, b in pairwise(page_set)]
    is_valid = all(adjacency != -1 for adjacency in adjacencies)
    return is_valid

def in_order(rules: list[tuple[PageNum, PageNum]], page_set: list[PageNum]) -> Generator[PageNum, None, None]:
    matrix = AdjacencyMatrix(page_set, rules)
    while len(page_set) > 0:
        other_pages = [(page_from, [page for page in page_set if page != page_from]) for page_from in page_set]
        _, first_page = sorted((sum(matrix.adjacencies(page, *rest)), page) for page, rest in other_pages).pop()
        yield first_page
        page_set.remove(first_page)

def load(filename: str) -> tuple[list[tuple[PageNum, PageNum]], list[list[PageNum]]]:
    with open(filename, 'r') as file:
        lines = iter(file)
        rule_lines = list(takewhile(lambda line: len(line.strip()) > 0, lines))
        page_lines = list(lines)
        rule_strings = [tuple(line.strip().split('|')) for line in rule_lines]
        rules = [(int(a), int(b)) for a, b in rule_strings]
        page_strings = [line.strip().split(',') for line in page_lines]
        page_sets = [[int(page) for page in line] for line in page_strings]
        return rules, page_sets

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='AOC2024-d05')
    parser.add_argument('filename')
    parser.add_argument('--debug', '-d', action="store_true")
    args = parser.parse_args()

    if (args.debug):
        def logd(*args):
            print(*args, file=sys.stderr)

    rules, page_sets = load(args.filename)

    valid_page_sets = [page_set for page_set in page_sets if valid(rules, page_set)]
    middle_pages = [page_set[int(len(page_set)/2)] for page_set in valid_page_sets]
    print(f"sum of middle pages: {sum(middle_pages)}")

    invalid_page_sets = [page_set for page_set in page_sets if not valid(rules, page_set)]
    resorted_page_sets = [list(in_order(rules, page_set)) for page_set in invalid_page_sets]
    resorted_middle_pages = [page_set[int(len(page_set)/2)] for page_set in resorted_page_sets]
    print(f"sum of resorted middle pages: {sum(resorted_middle_pages)}")
