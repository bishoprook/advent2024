from typing import Literal, Generator
from enum import Enum

class TokenType(Enum):
    """Enum representing the different meaningful tokens in the input."""
    MUL = (b'mul', 3)
    DO = (b'do', 2)
    NT = (b"n't", 3)
    OPAREN = (b'(', 1)
    COMMA = (b',', 1)
    CPAREN = (b')', 1)
    EOF = (None, 0)

type Token = TokenType | int | str

def decode_buffer(buffer: bytearray) -> str | int | None:
    """If buffer is empty, returns None. If numeric, returns the represented
    integer. Else returns as a UTF-8 string."""
    if len(buffer) == 0:
        return None
    text = buffer.decode('utf-8')
    return int(text) if text.isdigit() else text

def advance_to_next_delimiter(source) -> tuple[bytearray, TokenType]:
    """Advances position in `source` one byte at a time, storing those
    bytes in `buffer`, until a delimiter is reached. That will be either
    a recognized keyword token, or EOF. Returns both buffer and delimiter."""
    buffer = bytearray()
    while True:
        next_bytes = source.read(1)
        buffer.extend(next_bytes)
        for token_type in TokenType:
            t_bytes, width = token_type.value
            if width > 0 and buffer.endswith(t_bytes):
                return buffer.removesuffix(t_bytes), token_type
        if len(next_bytes) == 0:
            return buffer, TokenType.EOF

def read_all_tokens(source) -> Generator[Token, None, None]:
    """Reads source and produces a stream of tokens based on the problem
    statement."""
    while True:
        buffer, next_token = advance_to_next_delimiter(source)
        buffer_token = decode_buffer(buffer)
        if buffer_token is not None:
            yield buffer_token
        yield next_token
        if next_token is TokenType.EOF:
            return

OpCode = Enum('OpCode', ['MUL', 'DO', 'DONT'])
type Instruction = tuple[Literal[OpCode.MUL], int, int] | Literal[OpCode.DO, OpCode.DONT]

def parse(tokens: list[Token]) -> Generator[Instruction, None, None]:
    """Parse a sequence of tokens into a sequence of instructions."""
    T = TokenType
    idx = 0
    while True:
        match tokens[idx:]:
            case [T.EOF, *_]:
                return
            case [T.MUL, T.OPAREN, int(x), T.COMMA, int(y), T.CPAREN, *_]:
                yield (OpCode.MUL, x, y)
                idx += 6
            case [T.DO, T.OPAREN, T.CPAREN, *_]:
                yield OpCode.DO
                idx += 3
            case [T.DO, T.NT, T.OPAREN, T.CPAREN, *_]:
                yield OpCode.DONT
                idx += 3
            case _:
                idx += 1

def load_instructions(filename: str) -> list[Instruction]:
    """Open the file, tokenize, and parse the instructions."""
    with open(filename, 'rb') as file:
        tokens = list(read_all_tokens(file))
        return list(parse(tokens))

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
