from map import Map, Point

def logd(*_):
    pass

def load(filename: str) -> Map:
    with open(filename, 'r') as file:
        rows = list(file)
        return Map.parse(rows)

if __name__ == '__main__':
    import argparse
    import sys

    parser = argparse.ArgumentParser(prog='AOC2024-d05')
    parser.add_argument('filename')
    parser.add_argument('--debug', '-d', action="store_true")
    args = parser.parse_args()

    if (args.debug):
        def logd(*args):
            print(*args, file=sys.stderr)

    initial_map = load(args.filename)
    logd(initial_map)

    first_run_map = initial_map.clone()
    while first_run_map.guard_in_bounds():
        if args.debug:
            input("Press Enter to continue...")
        first_run_map.advance()
        logd(first_run_map)
    
    print(f"Unique path size: {first_run_map.visited_space_count()}")

    loop_trap_candidates = first_run_map.visited_spaces()
    initial_guard_pos, _ = initial_map.guard_state
    loop_trap_candidates.remove(initial_guard_pos)

    def is_loop_trap(i: int, candidate: Point) -> bool:
        print(f"\033[0KChecking candidate {i}/{len(loop_trap_candidates)}\033[1F", file=sys.stderr)
        test_map = initial_map.clone()
        test_map.set_obstacle(candidate)
        return test_map.run_to_end() == 'loop'
    
    loop_traps = [candidate for i, candidate in enumerate(loop_trap_candidates) if is_loop_trap(i, candidate)]
    print(f"\033[0KNumber of loop traps: {len(loop_traps)}")
