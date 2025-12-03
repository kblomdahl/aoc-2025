from sys import exit, stdin
from io import StringIO
from typing import Generator, List, TextIO
from functools import reduce
from math import log10, ceil

class Id:
    def __init__(self, value: int):
        self.value = value

    @staticmethod
    def from_str(s: str) -> 'Id':
        return Id(int(s))

def split_and_compare(value: int, part_size: int) -> bool:
    assert part_size > 0, "infinite loop guard"

    half = 10 ** part_size
    first = value % half
    remaining = value // half

    while remaining > 0:
        if remaining % half != first:
            return False
        remaining //= half

    return True

def is_invalid(value: int, largest_only: bool = True) -> bool:
    len = int(ceil(log10(value)))
    if len == 0:
        return False # single digit

    max_repeats = 3 if largest_only else len + 1

    for num_repeats in range(2, max_repeats):
        if len % num_repeats != 0:
            continue

        part_size = len // num_repeats

        if part_size == 0:
            print(value, largest_only, num_repeats, len, max_repeats)

        if split_and_compare(value, part_size):
            return True

    return False

class IdRange:
    def __init__(self, first: Id, last: Id):
        self.first = first
        self.last = last

    def invalid_ids(self, largest_only: bool = True) -> Generator[int, None, None]:
        for value in range(self.first.value, self.last.value + 1):
            if is_invalid(value, largest_only=largest_only):
                yield value

def parse_id_ranges(input: TextIO) -> List[IdRange]:
    lines = [line.strip() for line in input if line.strip()]

    def parse_id_range(s: str) -> IdRange:
        start_str, end_str = s.split("-")

        return IdRange(Id.from_str(start_str), Id.from_str(end_str))

    return reduce(
        lambda acc, x: acc + list([parse_id_range(s) for s in x.strip().split(",") if s]),
        lines,
        []
    )

def main() -> int:
    id_ranges = parse_id_ranges(stdin)

    print(sum(id for id_range in id_ranges for id in id_range.invalid_ids(largest_only=True)))
    print(sum(id for id_range in id_ranges for id in id_range.invalid_ids(largest_only=False)))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def example_input(self) -> List[IdRange]:
        lines = """
            11-22,95-115,998-1012,1188511880-1188511890,222220-222224,
            1698522-1698528,446443-446449,38593856-38593862,565653-565659,
            824824821-824824827,2121212118-2121212124
        """

        return parse_id_ranges(StringIO(lines))

    def test_example_1(self, example_input: List[IdRange]) -> None:
        assert sum(id for id_range in example_input for id in id_range.invalid_ids(largest_only=True)) == 1227775554

    def test_example_2(self, example_input: List[IdRange]) -> None:
        assert sum(id for id_range in example_input for id in id_range.invalid_ids(largest_only=False)) == 4174379265
