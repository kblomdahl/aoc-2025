from functools import cache
from sys import exit, stdin
from typing import List, Set

def starting_point(line: str) -> int:
    return line.index('S')

def tachyon_sim(lines: List[str], initial_beam: int) -> int:
    def tachyon_step(line: str, beams: Set[int]) -> tuple[Set[int], int]:
        new_beams: Set[int] = set()
        num_splits = 0

        for beam in beams:
            match line[beam]:
                case '^':
                    new_beams.add(beam - 1)
                    new_beams.add(beam + 1)
                    num_splits += 1
                case _:
                    new_beams.add(beam)

        return new_beams, num_splits

    total_splits = 0
    beams: Set[int] = {initial_beam}

    for line in lines:
        beams, num_splits = tachyon_step(line, beams)
        total_splits += num_splits

    return total_splits

def tachyon_quantum_sum(lines: List[str], starting_point: int) -> int:
    @cache
    def quantum_step(row: int, beam: int) -> int:
        if row == len(lines):
            return 1

        match lines[row][beam]:
            case '^':
                return quantum_step(row + 1, beam - 1) + quantum_step(row + 1, beam + 1)
            case _:
                return quantum_step(row + 1, beam)

    return quantum_step(1, starting_point)

def main() -> int:
    lines = [line.strip() for line in stdin if line.strip()]

    print(tachyon_sim(lines[1:], starting_point(lines[0])))
    print(tachyon_quantum_sum(lines[1:], starting_point(lines[0])))

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
        assert tachyon_quantum_sum(example_input[1:], starting_point(example_input[0])) == 40
