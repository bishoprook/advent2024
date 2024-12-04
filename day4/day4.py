from typing import Callable

def stencil_horizontal(lines: list[str], top: int, left: int) -> str:
    """Isolates a length 4 string going right from top/left."""
    return lines[top][left:left + 4]

def stencil_vertical(lines: list[str], top: int, left: int) -> str:
    """Isolates a length 4 string going down from top/left."""
    return (lines[top][left] +
            lines[top + 1][left] +
            lines[top + 2][left] +
            lines[top + 3][left])

def stencil_slash(lines: list[str], top: int, left: int) -> str:
    """Isolates a length 4 string going from top/right to bottom/left."""
    return (lines[top + 3][left] +
            lines[top + 2][left + 1] +
            lines[top + 1][left + 2] +
            lines[top][left + 3])

def stencil_backslash(lines: list[str], top: int, left: int) -> str:
    """Isolates a length 4 string going from top/left to bottom/right."""
    return (lines[top][left] +
            lines[top + 1][left + 1] +
            lines[top + 2][left + 2] +
            lines[top + 3][left + 3])

def stencil_x(lines: list[str], top: int, left: int) -> str:
    """Isolates a length 5 string from a 3x3 square in a Z pattern."""
    return (lines[top][left] +
            lines[top][left + 2] +
            lines[top + 1][left + 1] +
            lines[top + 2][left] +
            lines[top + 2][left + 2])

def apply_stencil(lines: list[str],
                  stencil: Callable[[list[str],int,int],str],
                  height: int,
                  width: int) -> list[str]:
    """Applies the given stencil with the given size to the full puzzle and
    returns the results."""
    return [stencil(lines, top, left)
            for left in range(len(lines[0]) - width + 1)
            for top in range(len(lines) - height + 1)]

def load_lines(filename: str) -> list[str]:
    """Opens the file and reads in the puzzle's horizontal lines."""
    with open(filename, 'r') as file:
        return list(line.strip() for line in file)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='AOC2024-d03')
    parser.add_argument('filename')
    args = parser.parse_args()

    lines = load_lines(args.filename)

    stencils = [(stencil_horizontal, 1, 4),
                (stencil_vertical, 4, 1),
                (stencil_slash, 4, 4),
                (stencil_backslash, 4, 4)]
    candidates = [c
                  for stencil, height, width in stencils
                  for c in apply_stencil(lines, stencil, height, width)]
    xmas_count = candidates.count('XMAS') + candidates.count('SAMX')
    print(f"XMAS count: {xmas_count}")

    # Stencil gives results in a Z shape. Valid X-MASes are:
    #  M M    S M    S S    M S
    #   A      A      A      A
    #  S S    S M    M M    M S
    #   =      =      =      =
    # MMASS  SMASM  SSAMM  MSAMS
    crosses = apply_stencil(lines, stencil_x, 3, 3)
    crossmas_count = (crosses.count('MMASS') + crosses.count('SMASM') +
                      crosses.count('SSAMM') + crosses.count('MSAMS'))
    print(f"Crossmas count: {crossmas_count}")
