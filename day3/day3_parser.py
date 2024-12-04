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

class Tokenizer(object):
    """An Iterable tokenizer that takes in a BufferedReader as a source. It
    yields a sequence of tokens based on the problem statement."""
    def __init__(self, source):
        self.source = source
        self.buffer = bytearray()
    
    def eof(self) -> bool:
        return len(self.source.peek(1)) == 0
    
    def advance(self, size = 1, buffer = True) -> None:
        """Advances by `size` bytes in the source. If `buffer` is true, the
        passed-over bytes will be stored in the local buffer. This handles
        strings and numbers that appear between specific tokens."""
        data = self.source.read(size)
        if buffer:
            self.buffer.extend(data)
    
    def next_token_type(self) -> TokenType | None:
        """Finds the TokenType associated with the bytes currently at the
        front of `self.source`, or `None` if there is no matching token."""
        for token_type in TokenType:
            token_bytes, width = token_type.value
            if width > 0 and self.source.peek(width)[:width] == token_bytes:
                return token_type

    def buffer_token(self) -> Generator[Token, None, None]:
        """Yields between 0 and 1 `Token`s: nothing if `self.buffer` is
        currently empty, otherwise either an `int` or `str` depending on the
        format of the data."""
        if len(self.buffer) == 0:
            return
        text = self.buffer.decode('utf-8')
        self.buffer.clear()
        yield int(text) if text.isdigit() else text

    def __iter__(self) -> Generator[Token, None, None]:
        """Produces a sequence of `Token`s until `self.source` reaches EOF.
        Then, yields at most one more `int` or `str` buffer token, and an EOF
        token."""
        while not self.eof():
            next_token_type = self.next_token_type()

            if next_token_type is None:
                self.advance()
                continue
            
            yield from self.buffer_token()
            yield next_token_type

            _, width = next_token_type.value
            self.advance(width, buffer=False)

        yield from self.buffer_token()
        yield TokenType.EOF

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
        tokens = list(Tokenizer(file))
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
