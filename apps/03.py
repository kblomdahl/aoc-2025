from sys import exit, stdin
from typing import Dict, List

def max_batteries(batteries: str, count: int) -> int:
    so_far: Dict[int, int] = {}

    for remaining_picks in range(0, count):
        max_previous_value = 0
        next_so_far = {}

        for i in reversed(range(len(batteries) - remaining_picks)):
            if so_far.get(i + 1, 0) > max_previous_value:
                max_previous_value = so_far[i + 1]

            next_so_far[i] = int(batteries[i] + str(max_previous_value if max_previous_value > 0 else ""))

        so_far = next_so_far

    return max(so_far.values())

def main() -> int:
    banks = [line.strip() for line in stdin if line.strip()]

    print(sum(b for b in [max_batteries(batteries, 2) for batteries in banks]))
    print(sum(b for b in [max_batteries(batteries, 12) for batteries in banks]))

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

        return list([line.strip() for line in lines if line.strip()])

    def test_example_1(self, example_input: List[str]) -> None:
        assert sum(max_batteries(batteries, 2) for batteries in example_input) == 357

    def test_example_2(self, example_input: List[str]) -> None:
        assert sum(max_batteries(batteries, 12) for batteries in example_input) == 3121910778619
