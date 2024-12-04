from typing import Iterable, Literal, Generator
from enum import Enum
from more_itertools import consume
from util import sliding_window

def logd(*_):
    pass

def tokenize(source: bytes) -> Generator[str, None, None]:
    delimiters = [b'mul', b'do', b"n't", b'(', b')', b',']
    buffer = bytearray()
    while True:
        next_byte = source.read(1)
        logd(f"\033[48;5;53mtokenizing:\033[0m {repr(next_byte)}")
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
        logd(f"\033[48;5;60m    lexing:\033[0m {repr(token)}")
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

def parse(lexes: Iterable[LexCode | int | str]) -> Generator[Instruction, None, None]:
    window = sliding_window(lexes, 6)
    for items in window:
        logd(f"\033[48;5;24m   parsing:\033[0m {repr(items)}")
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

def execute(instructions: Iterable[Instruction]) -> int:
    total, enabled = 0, True
    for instruction in instructions:
        logd(f"\033[48;5;18m executing:\033[0m {repr(instruction)}")
        match instruction:
            case (OpCode.MUL, a, b) if enabled:
                total += a * b
            case OpCode.DO:
                enabled = True
            case OpCode.DONT:
                enabled = False
    return total

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='AOC2024-d03')
    parser.add_argument('filename')
    parser.add_argument('--debug', '-d', action="store_true")
    args = parser.parse_args()

    if (args.debug):
        def logd(*args):
            print(*args, file=sys.stderr)

    # From the initial state, run every instruction in sequence.
    with open(args.filename, 'rb') as file:
        total = execute(parse(lex(tokenize(file))))
    
    print("Total: ", total)
