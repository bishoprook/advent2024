import unittest
from map import (turn_left,
                 turn_right,
                 forward,
                 facing_to_guard_char, 
                 guard_char_to_facing, 
                 find_in_grid, 
                 Map)

class MapTests(unittest.TestCase):
    def test_turn_right(self):
        self.assertEqual(turn_right('N'), 'E')
        self.assertEqual(turn_right('E'), 'S')
        self.assertEqual(turn_right('S'), 'W')
        self.assertEqual(turn_right('W'), 'N')

    def test_turn_left(self):
        self.assertEqual(turn_left('N'), 'W')
        self.assertEqual(turn_left('E'), 'N')
        self.assertEqual(turn_left('S'), 'E')
        self.assertEqual(turn_left('W'), 'S')

    def test_forward(self):
        self.assertEqual(forward((1, 1), 'N'), (0, 1))
        self.assertEqual(forward((1, 1), 'E'), (1, 2))
        self.assertEqual(forward((1, 1), 'S'), (2, 1))
        self.assertEqual(forward((1, 1), 'W'), (1, 0))

    def test_facing_to_guard_char(self):
        self.assertEqual(facing_to_guard_char('N'), '^')
        self.assertEqual(facing_to_guard_char('E'), '>')
        self.assertEqual(facing_to_guard_char('S'), 'v')
        self.assertEqual(facing_to_guard_char('W'), '<')

    def test_guard_char_to_facing(self):
        self.assertEqual(guard_char_to_facing('^'), 'N')
        self.assertEqual(guard_char_to_facing('>'), 'E')
        self.assertEqual(guard_char_to_facing('v'), 'S')
        self.assertEqual(guard_char_to_facing('<'), 'W')

    def test_find_in_grid(self):
        rows = ['#...',
                '..##',
                '#.<.']
        self.assertEqual(find_in_grid(rows, '#'), [(0, 0), (1, 2), (1, 3), (2, 0)])
        self.assertEqual(find_in_grid(rows, '^>v<'), [(2, 2)])
    
    def test_parse(self):
        rows = ['.#...',
                '....#',
                '#...<',
                '.##..']
        map = Map.parse(rows)
        self.assertEqual(map.width, 5)
        self.assertEqual(map.height, 4)
        self.assertTrue(map.is_obstacle((0, 1)))
        self.assertTrue(map.is_obstacle((1, 4)))
        self.assertTrue(map.is_obstacle((2, 0)))
        self.assertTrue(map.is_obstacle((3, 1)))
        self.assertTrue(map.is_obstacle((3, 2)))
        self.assertFalse(map.is_obstacle((0, 2)))
        self.assertFalse(map.is_obstacle((1, 0)))
        self.assertEqual(map.guard_state, ((2, 4), 'W'))
        self.assertTrue(map.is_visited((2, 4), 'W'))
        self.assertEqual(map.visited_count(), 1)

    def test_advance(self):
        rows = ['.#...',
                '....#',
                '#...<',
                '.##..']
        map = Map.parse(rows)
        map.advance()
        self.assertEqual(map.guard_state, ((2, 3), 'W'))
        self.assertTrue(map.is_visited((2, 3), 'W'))
        self.assertEqual(map.visited_count(), 2)
        for _ in range(10):
            map.advance()
        self.assertEqual(map.guard_state, ((3, 3), 'S'))
        self.assertEqual(map.visited_count(), 12)
        self.assertEqual(map.visited_space_count(), 8)
        map.advance()
        self.assertFalse(map.guard_in_bounds())
    
    def test_visited_spaces(self):
        rows = ['.#...',
                '....#',
                '#...<',
                '.##..']
        map = Map.parse(rows)
        for _ in range(4):
            map.advance()
        self.assertEqual([(2, 1), (2, 2), (2, 3), (2, 4)], map.visited_spaces())
    
    def test_is_in_loop(self):
        rows = ['.#...',
                '....#',
                '#.<..',
                '.#.#.']
        map = Map.parse(rows)
        for _ in range(9):
            self.assertFalse(map.is_in_loop())
            map.advance()
        self.assertTrue(map.is_in_loop())
    
    def test_run_to_end(self):
        looping_map = ['.#...',
                       '....#',
                       '#.<..',
                       '.#.#.']
        exiting_map = ['.#...',
                       '....#',
                       '#.<..',
                       '.##..']
        self.assertEqual('loop', Map.parse(looping_map).run_to_end())
        self.assertEqual('exit', Map.parse(exiting_map).run_to_end())

if __name__ == '__main__':
    unittest.main()

