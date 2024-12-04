from typing import Literal, Generator
import re

def tokenize(line: str) -> list[str]:
    """Given a line of input, find all occurrences of valid tokens. They must
    be `do()`, `don't()`, or `mul(X,Y)` where X and Y are integers from 1-3
    digits. No whitespace is allowed."""
    token_pattern = r"(?:mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\))"
    return [match.group() for match in re.finditer(token_pattern, line)]

Instruction = tuple[Literal['mul'], int, int] | tuple[Literal['do', "don't"]]

def parse(token: str) -> Instruction:
    """Given a token, parse and sanitize it into one of:
    * the tuple `('mul', a, b)` where a, b are the int operands
    * the tuple `('do')`
    * the tuple `("don't")`"""
    parse_pattern = r"(mul|do|don't)\((?:(\d{1,3}),(\d{1,3}))?\)"
    op, a, b = re.match(parse_pattern, token).groups()
    return (op, int(a), int(b)) if op == 'mul' else (op)

def load_instructions(filename: str) -> Generator[Instruction, None, None]:
    """Open the file, tokenize instructions, and parse each."""
    with open(filename, 'r') as file:
        for line in file:
            for token in tokenize(line):
                yield parse(token)

State = tuple[int, bool]

def initial_state() -> State:
    """The initial state when calculating the result. Total starts at 0, and
    mul operations are initially enabled."""
    return (0, True)

def next_state(state: State, instruction: Instruction) -> State:
    """Returns a new state for the current state and parsed instruction, or the
    same state if unchanged."""
    total, enabled = state
    match instruction:
        case ('mul', a, b):
            return (total + a * b, enabled) if enabled else state
        case ('do'):
            return (total, True)
        case ("don't"):
            return (total, False)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(prog='AOC2024-d03')
    parser.add_argument('filename')
    args = parser.parse_args()

    # From the initial state, run every instruction in sequence.
    state = initial_state()
    for instruction in load_instructions(args.filename):
        state = next_state(state, instruction)
    
    total, _ = state
    print("Total: ", total)
