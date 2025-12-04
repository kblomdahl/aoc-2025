from sys import exit, stdin
from typing import Generator, Dict, TextIO
from io import StringIO

type Coord = tuple[int, int]

def parse_map(input: TextIO) -> Dict[Coord, str]:
    lines = [line.strip() for line in input if line.strip()]

    return {
        (x, y): char
        for y, line in enumerate(lines)
        for x, char in enumerate(line)
    }

def count_paper(map: Dict[Coord, str]) -> int:
    return sum(1 for char in map.values() if char == "@")

def adjacent_coords(coord: Coord) -> Generator[Coord, None, None]:
    x, y = coord

    yield (x - 1, y - 1)
    yield (x - 1, y)
    yield (x - 1, y + 1)

    yield (x, y - 1)
    yield (x, y + 1)

    yield (x + 1, y - 1)
    yield (x + 1, y)
    yield (x + 1, y + 1)

def is_accessible_paper(map: Dict[Coord, str], coord: Coord) -> int:
    return sum(
        1
        for adjacent in adjacent_coords(coord)
        if map.get(adjacent) == "@"
    ) < 4

def remove_accessible_paper(map: Dict[Coord, str]) -> Dict[Coord, str]:
    return {
        coord: "." if char == "@" and is_accessible_paper(map, coord) else char
        for coord, char in map.items()
    }

def remove_all_accessible_paper(map: Dict[Coord, str]) -> Dict[Coord, str]:
    cleaned_map = map

    while True:
        new_map = remove_accessible_paper(cleaned_map)

        if count_paper(new_map) == count_paper(cleaned_map):
            break

        cleaned_map = new_map

    return cleaned_map

def main() -> int:
    map = parse_map(stdin)

    print(sum(1 for coord, char in map.items() if char == "@" and is_accessible_paper(map, coord)))
    print(count_paper(map) - count_paper(remove_all_accessible_paper(map)))

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
        assert sum(1 for coord, char in map.items() if char == "@" and is_accessible_paper(map, coord)) == 13

    def test_example_2(self, example_input: TextIO) -> None:
        map = parse_map(example_input)

        assert count_paper(map) - count_paper(remove_all_accessible_paper(map)) == 43
