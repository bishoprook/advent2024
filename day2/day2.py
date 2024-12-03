from typing import Generator, Literal, NewType

Level = NewType('Level', int)
Report = list[Level]

def load_reports(filename: str) -> Generator[Report, None, None]:
    """Opens the file and reads reports line by line.
    
    :param str filename: the input file to open
    :returns Generator[Report, None, None]: all the reports in sequence"""
    with open(filename, 'r') as file:
        for report_line in file:
            yield [int(level) for level in report_line.split()]

def valence(num: int) -> Literal[-1, 0, 1]:
    """Returns the valence of the number: -1 for negative numbers,
    1 for positive numbers, 0 for zero.
    
    :param int num: the input
    :returns int: -1 for negative, 1 for positive, 0 for zero"""
    return -1 if num < 0 else 1 if num > 0 else 0

def is_safe(report: Report) -> bool:
    """Check if a report is safe without attempting to repair. As defined in
    the problem statement, a report is safe if both are true:
    * The levels are either all increasing or all decreasing.
    * Any two adjacent levels differ by at least one and at most three.
    
    :param Report report: the report to check
    :returns bool: whether the report is safe"""

    # Find the difference between each element and the next. So for example,
    # [1, 3, 7, 6, 10] would become [2, 4, -1, 4]. This has a size 1 less than
    # the report.
    diffs = [b - a for a, b in zip(report, report[1:])]

    # We can immediately declare unsafe if any diff is not within range of
    # either [-3,-1] or [1,3].
    if any(diff < -3 or diff == 0 or diff > 3 for diff in diffs):
        return False

    # Find the valence of each diff. This tracks if the values are increasing,
    # decreasing, or staying the same. For example, [2, 4, -1, 4] would become
    # [1, 1, -1, 1].
    diff_valences = [valence(diff) for diff in diffs]

    # Ensure there are no locations where the valence of the diff changes. This
    # would represent a change in direction. For example, with the input
    # [2, 4, -1, 4], the diff valences are [1, 1, -1, 1], and the valence
    # changes between index 1-2 and 2-3.
    return all(a == b for a, b in zip(diff_valences, diff_valences[1:]))

def candidate_repairs(report: Report) -> Generator[Report, None, None]:
    """Gets all candidate versions of this report after undergoing at most one
    removal of a single level. For example, `[1, 3, 5, 7]` would yield the
    sequence `[1, 3, 5, 7]`, `[3, 5, 7]`, `[1, 5, 7]`, `[1, 3, 7]`,
    `[1, 3, 5]`.
    
    :param Report report: the report to evaluate
    :returns Generator[Report, None, None]: all valid repairs applied to
    the report"""
    yield report
    for drop_idx in range(len(report)):
        yield [level for i, level in enumerate(report) if i != drop_idx]

def is_safe_with_repair(report: Report) -> bool:
    """Checks whether this report is safe or it can be made safe with at most
    one repair.
    
    :param Report report: the report to evaluate
    :returns bool: whether the report is safe"""
    return any(is_safe(candidate) for candidate in candidate_repairs(report))

if __name__ == '__main__':
    import argparse
    from more_itertools import quantify

    parser = argparse.ArgumentParser(prog='AOC2024-d01')
    parser.add_argument('filename')
    args = parser.parse_args()

    safe_reports = quantify(load_reports(args.filename), is_safe_with_repair)
    print("Safe reports: ", safe_reports)