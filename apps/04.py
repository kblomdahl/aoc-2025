from sys import exit, stdin
from typing import Dict, TextIO
from io import StringIO

type Coord = tuple[int, int]

def parse_map(input: TextIO) -> Dict[Coord, int]:
    lines = [line.strip() for line in input if line.strip()]

    return {
        (x, y): 1
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
        if char == "@"
    }

def is_accessible_paper(map: Dict[Coord, int], coord: Coord) -> int:
    x, y = coord
    adjacent_papers = map.get((x - 1, y - 1), 0) \
        + map.get((x - 1, y), 0) \
        + map.get((x - 1, y + 1), 0) \
        + map.get((x, y - 1), 0) \
        + map.get((x, y + 1), 0) \
        + map.get((x + 1, y - 1), 0) \
        + map.get((x + 1, y), 0) \
        + map.get((x + 1, y + 1), 0)

    return adjacent_papers < 4

def remove_accessible_paper(map: Dict[Coord, int]) -> Dict[Coord, int]:
    return {
        coord: char
        for coord, char in map.items()
        if not is_accessible_paper(map, coord)
    }

def remove_all_accessible_paper(map: Dict[Coord, int]) -> Dict[Coord, int]:
    cleaned_map = map

    while (new_map := remove_accessible_paper(cleaned_map)) != cleaned_map:
        cleaned_map = new_map

    return cleaned_map

def main() -> int:
    map = parse_map(stdin)

    print(len(map) - len(remove_accessible_paper(map)))
    print(len(map) - len(remove_all_accessible_paper(map)))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def example_input(self) -> TextIO:
        content = """
            ..@@.@@@@.
            @@@.@.@.@@
            @@@@@.@.@@
            @.@@@@..@.
            @@.@@@@.@@
            .@@@@@@@.@
            .@.@.@.@@@
            @.@@@.@@@@
            .@@@@@@@@.
            @.@.@@@.@.
        """.strip()

        return StringIO(content)

    def test_example_1(self, example_input: TextIO) -> None:
        map = parse_map(example_input)
        assert len(map) - len(remove_accessible_paper(map)) == 13

    def test_example_2(self, example_input: TextIO) -> None:
        map = parse_map(example_input)

        assert len(map) - len(remove_all_accessible_paper(map)) == 43
