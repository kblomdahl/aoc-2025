from sys import exit, stdin
from typing import List, TextIO, Tuple
from dataclasses import dataclass
from itertools import combinations
from io import StringIO
from bisect import bisect_left, bisect_right
from functools import cache

type Tile = Tuple[int, int]

@dataclass(frozen=True, slots=True)
class Borders:
    horizontal_lines: Tuple[Tuple[Tile, Tile], ...]
    horizontal_edges: Tuple[Tuple[Tile, Tile], ...]
    vertical_lines: Tuple[Tuple[Tile, Tile], ...]
    vertical_edges: Tuple[Tuple[Tile, Tile], ...]

def parse_tile(line: str) -> Tile:
    x_str, y_str = line.strip().split(",")
    return (int(x_str), int(y_str))

def parse_tiles(content: TextIO) -> List[Tile]:
    return [parse_tile(line) for line in content if line.strip()]

def build_green_borders(tiles: List[Tile]) -> Borders:
    borders = [(a, b) for a, b in zip(tiles, tiles[1:] + [tiles[0]])]
    horizontal = [(a, b) if a[0] < b[0] else (b, a) for a, b in borders if a[1] == b[1]]
    vertical = [(a, b) if a[1] < b[1] else (b, a) for a, b in borders if a[0] == b[0]]

    return Borders(
        horizontal_lines=tuple(sorted(horizontal, key=lambda border: border[0][1])),
        horizontal_edges=tuple(sorted(horizontal, key=lambda border: border[0][0])),
        vertical_lines=tuple(sorted(vertical, key=lambda border: border[0][0])),
        vertical_edges=tuple(sorted(vertical, key=lambda border: border[0][1])),
    )

def rectangle_area(a: Tile, b: Tile) -> int:
    return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

def build_every_rectangle(tiles: List[Tile]) -> List[Tuple[Tile, Tile]]:
    return sorted(
        [(tiles[i], tiles[j]) for i, j in combinations(range(len(tiles)), 2)],
        key=lambda rect: rectangle_area(rect[0], rect[1]),
        reverse=True
    )

@cache
def point_inside_polygon_1d(
    borders: Tuple[Tuple[Tile, Tile], ...],
    x_index: int,
    x: int,
    y: int
) -> bool:
    upper = bisect_right(borders, x, key=lambda border: border[0][x_index])
    y_index = 1 - x_index
    inside = False

    for one, two in borders[:upper]:
        if not (one[y_index] <= y < two[y_index]):
            continue
        elif one[x_index] == x:
            return True

        inside = not inside

    return inside

@cache
def point_on_edge_1d(
    borders: Tuple[Tuple[Tile, Tile], ...],
    x_index: int,
    x: int,
    y: int,
) -> bool:
    lower = bisect_left(borders, x, key=lambda border: border[0][x_index])
    upper = bisect_right(borders, x, key=lambda border: border[0][x_index])
    y_index = 1 - x_index

    return any(one[y_index] <= y <= two[y_index] for one, two in borders[lower:upper])

def line_inside_polygon(
    borders: Borders,
    ax: int,
    ay: int,
    bx: int,
    by: int
) -> bool:
    if ax == bx:
        upper = bisect_right(borders.horizontal_edges, ax, key=lambda border: border[0][0])

        return all(
            point_inside_polygon_1d(borders.horizontal_lines, 1, y, ax)
            or point_on_edge_1d(borders.vertical_lines, 0, ax, y)
            for one, two in borders.horizontal_edges[:upper]
            for y in [one[1] - 1, one[1] + 1]
            if one[0] <= ax <= two[0] and (ay <= y <= by)
        )
    elif ay == by:
        upper = bisect_right(borders.vertical_edges, ay, key=lambda border: border[0][1])

        return all(
            point_inside_polygon_1d(borders.vertical_lines, 0, x, ay)
            or point_on_edge_1d(borders.horizontal_lines, 1, ay, x)
            for one, two in borders.vertical_edges[:upper]
            for x in [one[0] - 1, one[0] + 1]
            if one[1] <= ay <= two[1] and ax <= x <= bx
        )
    else:
        raise ValueError("only horizontal or vertical lines are supported")

def rectangle_inside(
    borders: Borders,
    a: Tile,
    b: Tile
) -> bool:
    min_x, max_x = min(a[0], b[0]), max(a[0], b[0])
    min_y, max_y = min(a[1], b[1]), max(a[1], b[1])

    if not line_inside_polygon(borders, min_x, min_y, min_x, max_y):
        return False
    if not line_inside_polygon(borders, min_x, max_y, max_x, max_y):
        return False
    if not line_inside_polygon(borders, max_x, min_y, max_x, max_y):
        return False
    if not line_inside_polygon(borders, min_x, min_y, max_x, min_y):
        return False
    return True

def main() -> int:
    tiles = parse_tiles(stdin)
    rectangles, green_borders = build_every_rectangle(tiles), build_green_borders(tiles)

    print(rectangle_area(*rectangles[0]))
    print(next(rectangle_area(a, b) for a, b in rectangles if rectangle_inside(green_borders, a, b)))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def tiles(self) -> List[Tile]:
        content = """
            7,1
            11,1
            11,7
            9,7
            9,5
            2,5
            2,3
            7,3
        """.strip()

        return parse_tiles(StringIO(content))

    def test_example_1(self, tiles: List[Tile]) -> None:
        rectangles = build_every_rectangle(tiles)

        assert max(rectangle_area(a, b) for a, b in rectangles) == 50

    def test_example_2(self, tiles: List[Tile]) -> None:
        rectangles, green_borders = build_every_rectangle(tiles), build_green_borders(tiles)

        assert next(rectangle_area(a, b) for a, b in rectangles if rectangle_inside(green_borders, a, b)) == 24
