from typing import Callable

def stencil_horizontal(lines: list[str], top: int, left: int) -> str:
    return lines[top][left:left + 4]

def stencil_vertical(lines: list[str], top: int, left: int) -> str:
    return lines[top][left] + lines[top + 1][left] + lines[top + 2][left] + lines[top + 3][left]

def stencil_slash(lines: list[str], top: int, left: int) -> str:
    return lines[top + 3][left] + lines[top + 2][left + 1] + lines[top + 1][left + 2] + lines[top][left + 3]

def stencil_backslash(lines: list[str], top: int, left: int) -> str:
    return lines[top][left] + lines[top + 1][left + 1] + lines[top + 2][left + 2] + lines[top + 3][left + 3]

def stencil_x(lines: list[str], top: int, left: int) -> str:
    return (
        lines[top][left] + lines[top][left + 2] +
        lines[top + 1][left + 1] +
        lines[top + 2][left] + lines[top + 2][left + 2]
    )

def apply_stencil(lines: list[str], stencil: Callable[[list[str],int,int],str], height: int, width: int) -> list[str]:
    return [stencil(lines, top, left) for left in range(len(lines[0]) - width + 1) for top in range(len(lines) - height + 1)]

def load_lines(filename: str) -> list[str]:
    """Opens the file and reads in the word search puzzle's horizontal lines.
    
    :param str filename: the input file to open
    :returns list[str]: the horizontal lines in the word search"""
    with open(filename, 'r') as file:
        return list(line.strip() for line in file)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='AOC2024-d03')
    parser.add_argument('filename')
    args = parser.parse_args()

    lines = load_lines(args.filename)

    horizontals = apply_stencil(lines, stencil_horizontal, 1, 4)
    verticals = apply_stencil(lines, stencil_vertical, 4, 1)
    slashes = apply_stencil(lines, stencil_slash, 4, 4)
    backslashes = apply_stencil(lines, stencil_backslash, 4, 4)
    combined = horizontals + verticals + slashes + backslashes
    xmas_count = combined.count('XMAS') + combined.count('SAMX')
    print(f"XMAS count: {xmas_count}")

    crosses = apply_stencil(lines, stencil_x, 3, 3)
    crossmas_count = crosses.count('MMASS') + crosses.count('SMASM') + crosses.count('SSAMM') + crosses.count('MSAMS')
    print(f"Crossmas count: {crossmas_count}")
