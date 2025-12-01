from sys import exit, stdin
from typing import Callable, List, Generator

def range_F100(start: int, steps: int, op: Callable[[int], int]) -> Generator[tuple[int, bool], None, None]:
    while steps > 0:
        if steps > 100:
            steps -= 100
            yield 0, steps != 0  # slight optimization since we only care about zero
        else:
            steps -= 1
            start = op(start) % 100
            yield start, steps != 0

def turn_dial(current: int, instr: str) -> Generator[tuple[int, bool], None, None]:
    match instr[0]:
        case "L":
            yield from range_F100(current, int(instr[1:]), lambda x: x - 1)
        case "R":
            yield from range_F100(current, int(instr[1:]), lambda x: x + 1)
        case _:
            raise ValueError(f"Invalid instruction: {instr}")

def turn_dials(directions: List[str], dial_position: int) -> Generator[tuple[int, bool], None, None]:
    for direction in directions:
        for new_position, is_intermediate in turn_dial(dial_position, direction):
            dial_position = new_position
            yield dial_position, is_intermediate

def main() -> int:
    lines = [line.strip() for line in stdin if line.strip()]

    print(sum(1 for new_position, is_intermediate in turn_dials(lines, 50) if new_position == 0 and not is_intermediate))
    print(sum(1 for new_position, _ in turn_dials(lines, 50) if new_position == 0))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def example_input(self) -> List[str]:
        lines = """
            L68
            L30
            R48
            L5
            R60
            L55
            L1
            L99
            R14
            L82
        """.strip().splitlines()

        return list(map(str.strip, lines))

    def test_example_1(self, example_input: List[str]) -> None:
        assert sum(1 for new_position, is_intermediate in turn_dials(example_input, 50) if new_position == 0 and not is_intermediate) == 3

    def test_example_2(self, example_input: List[str]) -> None:
        assert sum(1 for new_position, _ in turn_dials(example_input, 50) if new_position == 0) == 6
