import argparse

# Parse the command line arguments.
parser = argparse.ArgumentParser(prog='AOC2024-d01')
parser.add_argument('filename')
args = parser.parse_args()

# Open the file and read line by line. Each report is a space-separated list of
# levels.
with open(args.filename, 'r') as file:
    reports = [[int(level) for level in line.split()] for line in file]

# Return -1 for negative numbers, 1 for positive numbers, 0 for zero.
def valence(num):
    return -1 if num < 0 else 1 if num > 0 else 0

# Check if a report is safe without attempting to repair. As defined in the
# problem statement...
#   A report only counts as safe if both of the following are true:
#    * The levels are either all increasing or all decreasing.
#    * Any two adjacent levels differ by at least one and at most three.
def is_safe(report):
    # Find the difference between each element and the next. So for example,
    # [1, 3, 7, 6, 10] would become [2, 4, -1, 4]. This has a size 1 less than
    # the report.
    diffs = [b - a for a, b in zip(report, report[1:])]

    # Can immediately declare unsafe if any diff is not within range of either
    # [-3,-1] or [1,3].
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

# Return all candidate versions of this report after undergoing at most one
# removal of a single level. For example, [1, 3, 5, 7] would yield the sequence
# [1, 3, 5, 7], [3, 5, 7], [1, 5, 7], [1, 3, 7], [1, 3, 5].
def candidate_repairs(report):
    yield report
    for drop_idx in range(len(report)):
        yield [level for i, level in enumerate(report) if i != drop_idx]

# Returns whether a given report is safe using the safety rules described above
# and allowing up to one deletion of a level from the report.
def is_safe_with_repair(report):
    return any(is_safe(candidate) for candidate in candidate_repairs(report))

safe_reports = [report for report in reports if is_safe_with_repair(report)]
print("Safe reports: ", len(safe_reports))
