from typing import Iterable, Literal, Generator
from enum import Enum
from itertools import islice
from more_itertools import consume
import collections

def tokenize(source: bytes) -> Generator[str, None, None]:
    delimiters = [b'mul', b'do', b"n't", b'(', b')', b',']
    buffer = bytearray()
    while True:
        next_byte = source.read(1)
        buffer.extend(next_byte)
        for delimiter in delimiters:
            if buffer.endswith(delimiter):
                buffer_str = buffer.removesuffix(delimiter).decode()
                if len(buffer_str) > 0:
                    yield buffer_str
                yield delimiter.decode()
                buffer.clear()
        if len(next_byte) == 0:
            if len(buffer) > 0:
                yield buffer.decode()
            return

LexCode = Enum('LexCode', ['MUL', 'DO', 'NT', 'OP', 'CP', 'COMMA'])

def lex(tokens: Iterable[str]) -> Generator[LexCode | int | str, None, None]:
    for token in tokens:
        match token:
            case 'mul': yield LexCode.MUL
            case 'do': yield LexCode.DO
            case "n't": yield LexCode.NT
            case '(': yield LexCode.OP
            case ')': yield LexCode.CP
            case ',': yield LexCode.COMMA
            case str(n) if n.isdigit(): yield int(n)
            case _: yield token

OpCode = Enum('OpCode', ['MUL', 'DO', 'DONT'])
type Instruction = tuple[Literal[OpCode.MUL], int, int] | Literal[OpCode.DO, OpCode.DONT]

# Slight tweak from more_itertools
def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG EFG FG G ()
    iterator = iter(iterable)
    window = collections.deque(islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)
    while len(window) > 0:
        window.popleft()
        yield tuple(window)

def parse(lexes: Iterable[LexCode | int | str]) -> Generator[Instruction, None, None]:
    window = sliding_window(lexes, 6)
    for items in window:
        match items:
            case [LexCode.MUL, LexCode.OP, int(x), LexCode.COMMA, int(y), LexCode.CP, *_]:
                yield (OpCode.MUL, x, y)
                consume(window, 5)
            case [LexCode.DO, LexCode.OP, LexCode.CP, *_]:
                yield OpCode.DO
                consume(window, 2)
            case [LexCode.DO, LexCode.NT, LexCode.OP, LexCode.CP, *_]:
                yield OpCode.DONT
                consume(window, 2)

def load_instructions(filename: str) -> list[Instruction]:
    """Open the file, tokenize, and parse the instructions."""
    with open(filename, 'rb') as file:
        tokens = tokenize(file)
        lexes = lex(tokens)
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
