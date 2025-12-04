from sys import exit, stdin
from typing import List
from functools import cache

def to_int(numbers: List[int]) -> int:
    return sum(n * (10 ** i) for i, n in enumerate(reversed(numbers)))

@cache
def max_batteries(batteries: str, count: int) -> List[int]:
    if not batteries or count == 0:
        return []

    return max(
        (
            [int(n)] + max_batteries(batteries[index + 1:], count - 1)
            for index, n in enumerate(batteries)
        ),
        key=lambda x: (len(x), x)
    )

def main() -> int:
    banks = [line.strip() for line in stdin if line.strip()]

    print(sum(to_int(b) for b in [max_batteries(batteries, 2) for batteries in banks]))
    print(sum(to_int(b) for b in [max_batteries(batteries, 12) for batteries in banks]))
    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def example_input(self) -> List[str]:
        lines = """
            987654321111111
            811111111111119
            234234234234278
            818181911112111
        """.strip().splitlines()

        return list(map(str.strip, lines))

    def test_example_1(self, example_input: List[str]) -> None:
        banks = [line.strip() for line in example_input if line.strip()]
        chosen_batteries = [max_batteries(batteries, 2) for batteries in banks]

        assert sum(to_int(b) for b in chosen_batteries) == 357

    def test_example_2(self, example_input: List[str]) -> None:
        banks = [line.strip() for line in example_input if line.strip()]
        chosen_batteries = [max_batteries(batteries, 12) for batteries in banks]

        assert sum(to_int(b) for b in chosen_batteries) == 3121910778619
