from sys import exit, stdin
from typing import Callable, List, TextIO
from dataclasses import dataclass
from itertools import takewhile
from io import StringIO

@dataclass
class IngredientRange:
    start: int
    end: int

    def mergable(self, other: 'IngredientRange') -> bool:
        return (self.start <= other.start <= self.end) or \
            (other.start <= self.start <= other.end)

    def __len__(self) -> int:
        return (self.end - self.start) + 1

def parse_ingredients(input: TextIO) -> tuple[List[IngredientRange], List[int]]:
    ranges = [
        IngredientRange(*map(int, line.strip().split("-")))
        for line in takewhile(str.strip, input)
    ]

    return (
        ranges,
        [int(line.strip()) for line in input if line.strip()]
    )

def is_fresh(ingredient: int, ranges: List[IngredientRange]) -> bool:
    return any(r.start <= ingredient <= r.end for r in ranges)

def compact_ranges(ranges: List[IngredientRange]) -> List[IngredientRange]:
    result: List[IngredientRange] = []

    for current in ranges:
        to_merge = [other for other in result if current.mergable(other)]
        to_merge.append(current)

        result = [other for other in result if not current.mergable(other)]
        result.append(IngredientRange(
            min(r.start for r in to_merge),
            max(r.end for r in to_merge))
        )

    return result

def main() -> int:
    ranges, ingredients = parse_ingredients(stdin)
    ranges = compact_ranges(ranges)

    print(sum(1 for ingredient in ingredients if is_fresh(ingredient, ranges)))
    print(sum(len(r) for r in ranges))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def example_input(self) -> tuple[List[IngredientRange], List[int]]:
        content = """
            3-5
            10-14
            16-20
            12-18

            1
            5
            8
            11
            17
            32
        """.strip()

        return parse_ingredients(StringIO(content))

    def test_example_1(self, example_input: tuple[List[IngredientRange], List[int]]) -> None:
        ingredient_ranges, ingredients = example_input

        assert len(ingredient_ranges) == 4
        assert len(ingredients) == 6
        assert sum(1 for ingredient in ingredients if is_fresh(ingredient, ingredient_ranges)) == 3

    def test_example_2(self, example_input: tuple[List[IngredientRange], List[int]]) -> None:
        ingredient_ranges, _ = example_input

        assert sum(len(r) for r in compact_ranges(ingredient_ranges)) == 14
