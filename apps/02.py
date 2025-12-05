from dataclasses import dataclass
from sys import exit, stdin, maxsize
from io import StringIO
from typing import Generator, List, TextIO, Set
from functools import reduce

@dataclass
class IdRange:
    first: int
    last: int

    def prefixes(self) -> Generator[int, None, None]:
        last = str(self.last)
        first = str(self.first).rjust(len(last), "0")

        for i in range((len(last) + 1) // 2):
            start = int(first[:i + 1])
            stop = int(last[:i + 1]) + 1

            yield from range(start if start > 0 else 1, stop)

    def invalid_ids(self, max_repeats: int | None = None) -> Set[int]:
        result = set()

        for prefix in self.prefixes():
            remaining_repeats = max_repeats - 1 if max_repeats is not None else maxsize
            current = str(prefix) * 2

            while (current_value := int(current)) <= self.last and remaining_repeats > 0:
                if self.first <= current_value <= self.last:
                    result.add(current_value)

                remaining_repeats -= 1
                current += str(prefix)

        return result

def parse_id_ranges(input: TextIO) -> List[IdRange]:
    return [
        IdRange(*map(int, s.split("-")))
        for x in input
        for s in x.strip().split(",") if s
    ]

def main() -> int:
    id_ranges = parse_id_ranges(stdin)

    print(sum(id for id_range in id_ranges for id in id_range.invalid_ids(2)))
    print(sum(id for id_range in id_ranges for id in id_range.invalid_ids()))

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
        assert sum(id for id_range in example_input for id in id_range.invalid_ids(2)) == 1227775554

    def test_example_2(self, example_input: List[IdRange]) -> None:
        assert sum(id for id_range in example_input for id in id_range.invalid_ids()) == 4174379265
