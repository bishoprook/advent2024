from typing import Literal, Generator
from enum import Enum
import re

def tokenize(line: str) -> list[str]:
    """Produces a list of tokens delimited according to the problem
    statement."""
    return [t for t in re.split(r"(mul|do|n't|[(),])", line) if len(t) > 0]

LexCode = Enum('LexCode', ['MUL', 'DO', 'NT', 'OPAREN', 'CPAREN', 'COMMA'])

def lex(token: str) -> LexCode | int | str:
    match token:
        case 'mul': return LexCode.MUL
        case 'do': return LexCode.DO
        case "n't": return LexCode.NT
        case '(': return LexCode.OP
        case ')': return LexCode.CP
        case ',': return LexCode.COMMA
        case str(n) if n.isdigit(): return int(n)
        case _: return token

OpCode = Enum('OpCode', ['MUL', 'DO', 'DONT'])
type Instruction = tuple[Literal[OpCode.MUL], int, int] | Literal[OpCode.DO, OpCode.DONT]

def parse(lexes: list[LexCode | int | str]) -> Generator[Instruction, None, None]:
    while len(lexes) > 0:
        match lexes:
            case [LexCode.MUL, LexCode.OP, int(x), LexCode.COMMA, int(y), LexCode.CP, *_]:
                yield (OpCode.MUL, x, y)
                lexes = lexes[6:]
            case [LexCode.DO, LexCode.OP, LexCode.CP, *_]:
                yield OpCode.DO
                lexes = lexes[3:]
            case [LexCode.DO, LexCode.NT, LexCode.OP, LexCode.CP, *_]:
                yield OpCode.DONT
                lexes = lexes[3:]
            case _:
                lexes = lexes[1:]

def load_instructions(filename: str) -> list[Instruction]:
    """Open the file, tokenize, and parse the instructions."""
    with open(filename, 'r') as file:
        tokens = [token for line in file for token in tokenize(line)]
        lexes = [lex(token) for token in tokens]
        instructions = list(parse(lexes))
        return instructions

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
        case (OpCode.MUL, a, b):
            return (total + a * b, enabled) if enabled else state
        case OpCode.DO:
            return (total, True)
        case OpCode.DONT:
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
