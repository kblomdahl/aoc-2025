from sys import exit, stdin
from typing import List, Generator
from math import prod
from re import match

def parse_prefixed_int(s: str) -> str:
    if (m := match(r"\s*\d+", s)) is not None:
        return m.group(0)
    raise ValueError(f"invalid cephalopod number: {s[:10]}...")

def shuffle_numbers(numbers: List[str]) -> List[str]:
    max_length = max(len(num) for num in numbers)
    numbers = [num.ljust(max_length, " ") for num in numbers]

    return [
        "".join([numbers[row][column] for row in range(len(numbers))])
        for column in range(max_length)
    ]

def solve_homework(lines: List[str], rtl: bool = False) -> Generator[int, None, None]:
    for i, op in [(i, op) for i, op in enumerate(lines[-1]) if op in "*+"]:
        parts = [parse_prefixed_int(part[i:]) for part in lines[:-1]]

        if rtl:
            parts = shuffle_numbers(parts)

        match op:
            case "*":
                yield prod(map(int, parts))
            case "+":
                yield sum(map(int, parts))

def main() -> int:
    lines = [line for line in stdin if line.strip()]

    print(sum(answer for answer in solve_homework(lines)))
    print(sum(answer for answer in solve_homework(lines, rtl=True)))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def example_input(self) -> List[str]:
        lines = """
            123 328  51 64 
             45 64  387 23 
              6 98  215 314
            *   +   *   +  
        """.splitlines()

        return list([line for line in lines if line.strip()])

    def test_example_1(self, example_input: List[str]) -> None:
        assert sum(answer for answer in solve_homework(example_input)) == 4277556

    def test_example_2(self, example_input: List[str]) -> None:
        assert sum(answer for answer in solve_homework(example_input, rtl=True)) == 3263827
