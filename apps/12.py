from dataclasses import dataclass
from io import StringIO
from sys import exit, stdin
from typing import List, Tuple, TextIO, Dict
from re import fullmatch

@dataclass(frozen=True, slots=True)
class Presents:
    shapes: Dict[int, List[Tuple[int, int]]]
    regions: List[Tuple[Tuple[int, int], Tuple[int, ...]]]

def parse_shape(input: TextIO) -> List[Tuple[int, int]]:
    shape = list[Tuple[int, int]]()

    for y, line in enumerate(input):
        line = line.strip()
        if not line:
            break

        shape.extend((x, y) for x, c in enumerate(line) if c == "#")

    return shape

def parse_presents(input: TextIO) -> Presents:
    shapes, regions = {}, []

    for line in input:
        line = line.strip()

        if m := fullmatch(r"(\d+):", line):
            shapes[int(m[1])] = parse_shape(input)
        elif m := fullmatch(r"(\d+)x(\d+):((\s\d+)+)", line):
            width, height = int(m[1]), int(m[2])
            region_shapes = tuple(map(int, m[3].strip().split()))
            regions.append(((width, height), region_shapes))

    return Presents(shapes, regions)

def region_packable(
    region: Tuple[Tuple[int, int], Tuple[int, ...]],
    shapes: Dict[int, List[Tuple[int, int]]]
) -> bool:
    (width, height), shape_counts = region
    total_area = sum(
        len(shapes[i]) * count
        for i, count in enumerate(shape_counts)
        )

    return total_area <= width * height

def main() -> int:
    presents = parse_presents(stdin)

    print(sum(1 for region in presents.regions if region_packable(region, presents.shapes)))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def presents(self) -> Presents:
        lines = """
            0:
            ###
            ##.
            ##.

            1:
            ###
            ##.
            .##

            2:
            .##
            ###
            ##.

            3:
            ##.
            ###
            ##.

            4:
            ###
            #..
            ###

            5:
            ###
            .#.
            ###

            4x4: 0 0 0 0 2 0
            12x5: 1 0 1 0 2 2
            12x5: 1 0 1 0 3 2
        """.strip()

        return parse_presents(StringIO(lines))

    def test_example_1(self, presents: Presents) -> None:
        assert sum(1 for region in presents.regions if region_packable(region, presents.shapes)) == 2
