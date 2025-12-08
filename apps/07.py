from functools import cache
from sys import exit, stdin
from typing import Dict, List

def starting_point(line: str) -> int:
    return line.index('S')

def tachyon_sim(lines: List[str], initial_beam: int, trace_path: bool = False) -> int:
    so_far: Dict[tuple[int, int], int] = {}

    def tachyon_step(row: int, beam: int) -> int:
        if row == len(lines):
            return 1 if trace_path else 0
        elif (row, beam) in so_far:
            return so_far[(row, beam)] if trace_path else 0

        match lines[row][beam]:
            case '^':
                result = tachyon_step(row + 1, beam - 1) + tachyon_step(row + 1, beam + 1) + (0 if trace_path else 1)
            case _:
                result = tachyon_step(row + 1, beam)

        so_far[(row, beam)] = result
        return result

    return tachyon_step(0, initial_beam)

def main() -> int:
    lines = [line.strip() for line in stdin if line.strip()]

    print(tachyon_sim(lines[1:], starting_point(lines[0])))
    print(tachyon_sim(lines[1:], starting_point(lines[0]), trace_path=True))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def example_input(self) -> List[str]:
        lines = """
            .......S.......
            ...............
            .......^.......
            ...............
            ......^.^......
            ...............
            .....^.^.^.....
            ...............
            ....^.^...^....
            ...............
            ...^.^...^.^...
            ...............
            ..^...^.....^..
            ...............
            .^.^.^.^.^...^.
            ...............
        """.splitlines()

        return list([line.strip() for line in lines if line.strip()])

    def test_example_1(self, example_input: List[str]) -> None:
        assert tachyon_sim(example_input[1:], starting_point(example_input[0])) == 21

    def test_example_2(self, example_input: List[str]) -> None:
        assert tachyon_sim(example_input[1:], starting_point(example_input[0]), trace_path=True) == 40
