from typing import Literal, Self

type Point = tuple[int, int]
type Facing = Literal['N', 'E', 'S', 'W']

def turn_right(facing: Facing) -> Facing:
    return {'N':'E', 'E':'S', 'S':'W', 'W':'N'}[facing]

def turn_left(facing: Facing) -> Facing:
    return {'N':'W', 'E':'N', 'S':'E', 'W':'S'}[facing]

def forward(pos: Point, facing: Facing) -> Point:
    top, left = pos
    dTop, dLeft = {'N':(-1,0), 'E':(0,1), 'S':(1,0), 'W':(0,-1)}[facing]
    return (top + dTop, left + dLeft)

type GuardChar = Literal['^', '>', 'v', '<']
type GuardState = tuple[Point, Facing]

def facing_to_guard_char(facing: Facing) -> GuardChar:
    return {'N':'^', 'E':'>', 'S':'v', 'W':'<'}[facing]

def guard_char_to_facing(guard_char: GuardChar) -> Facing:
    return {'^':'N', '>':'E', 'v':'S', '<':'W'}[guard_char]

def find_in_grid(rows: list[str], search_chars: str) -> list[Point]:
    return [(top, left) for top, row in enumerate(rows) for left, char in enumerate(row) if char in search_chars]

class Map(object):
    @classmethod
    def parse(self, rows: list[str]) -> Self:
        height, width = len(rows), len(rows[0])
        obstacles = find_in_grid(rows, '#')
        guard_top, guard_left = find_in_grid(rows, '^>v<')[0]
        guard_facing = guard_char_to_facing(rows[guard_top][guard_left])
        return Map(height, width, obstacles, ((guard_top, guard_left), guard_facing))

    def __init__(self, height: int, width: int, obstacles: list[Point], guard_state: GuardState):
        self.height = height
        self.width = width
        self.obstacles = obstacles
        self.guard_state = guard_state
        self.__obstacle_map__ = [[False for left in range(width)] for top in range(height)]
        for pos in obstacles:
            self.set_obstacle(pos)
        self.__visited_map__ = [[{'N':False, 'E':False, 'S':False, 'W':False} for _ in range(width)] for _ in range(height)]
        self.set_visited(*guard_state)
    
    def clone(self) -> Self:
        return Map(self.height, self.width, self.obstacles, self.guard_state)
    
    def in_bounds(self, pos: Point) -> bool:
        top, left = pos
        return top >= 0 and top < self.height and left >= 0 and left < self.width
    
    def guard_in_bounds(self) -> bool:
        pos, _ = self.guard_state
        return self.in_bounds(pos)
    
    def is_obstacle(self, pos: Point) -> bool:
        if not self.in_bounds(pos):
            return False
        top, left = pos
        return self.__obstacle_map__[top][left]
    
    def set_obstacle(self, pos: Point):
        if not self.in_bounds(pos):
            return
        top, left = pos
        self.__obstacle_map__[top][left] = True
    
    def is_visited(self, pos: Point, facing: Facing) -> bool:
        if not self.in_bounds(pos):
            return False
        top, left = pos
        return self.__visited_map__[top][left][facing]
    
    def is_visited_space(self, pos: Point) -> bool:
        if not self.in_bounds(pos):
            return False
        top, left = pos
        return any(self.__visited_map__[top][left].values())
    
    def set_visited(self, pos: Point, facing: Facing):
        if not self.in_bounds(pos):
            return
        top, left = pos
        self.__visited_map__[top][left][facing] = True

    def visited_count(self):
        return sum(1
                   for top in range(self.height)
                   for left in range(self.width)
                   for dir in 'NESW'
                   if self.is_visited((top, left), dir))

    def visited_space_count(self):
        return sum(1
                   for top in range(self.height)
                   for left in range(self.width)
                   if self.is_visited_space((top, left)))

    def visited_spaces(self):
        return [(top, left)
                for top in range(self.height)
                for left in range(self.width)
                if self.is_visited_space((top, left))]
    
    def advance(self):
        if not self.guard_in_bounds():
            return
        pos, facing = self.guard_state
        in_front = forward(pos, facing)
        if self.is_obstacle(in_front):
            self.guard_state = (pos, turn_right(facing))
        else:
            self.guard_state = (in_front, facing)
        self.set_visited(*self.guard_state)
    
    def is_in_loop(self):
        if not self.guard_in_bounds():
            return False
        pos, facing = self.guard_state
        in_front = forward(pos, facing)
        return self.is_visited(in_front, facing)
    
    def run_to_end(self) -> Literal['exit', 'loop']:
        while not self.is_in_loop() and self.guard_in_bounds():
            self.advance()
        return 'loop' if self.is_in_loop() else 'exit'

    def __char__(self, pos: Point) -> str:
        guard_pos, facing = self.guard_state
        if pos == guard_pos:
            return facing_to_guard_char(facing)
        elif self.is_obstacle(pos):
            return '#'
        elif self.is_visited_space(pos):
            return 'o'
        else:
            return '.'

    def __str__(self):
        return '\n'.join(''.join(self.__char__((top, left)) for left in range(self.width)) for top in range(self.height))
