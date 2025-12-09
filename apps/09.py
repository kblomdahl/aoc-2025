from sys import exit, stdin
from typing import List, TextIO, Tuple
from dataclasses import dataclass
from itertools import combinations
from io import StringIO

@dataclass(frozen=True, slots=True)
class Tile:
    x: int
    y: int

def parse_tiles(content: TextIO) -> List[Tile]:
    return [Tile(*map(int, line.strip().split(","))) for line in content if line.strip()]

def build_green_borders(tiles: List[Tile]) -> List[Tuple[Tile, Tile]]:
    return [(a, b) for a, b in zip(tiles, tiles[1:] + [tiles[0]])]

def build_every_rectangle(tiles: List[Tile]) -> List[Tuple[Tile, Tile]]:
    return [
        (tiles[i], tiles[j])
        for i, j in combinations(range(len(tiles)), 2)
    ]

def point_inside_polygon_1d(
    borders_1d: List[int],
    x: int,
) -> bool:
    inside = False

    for border in borders_1d:
        if border < x:
            inside = not inside
        elif border == x:
            inside = True
            break # on edge

    return inside

def point_on_edge_1d(
    borders_1d: List[Tuple[int, int]],
    x: int,
) -> bool:
    on_edge = any(
        min(one, two) <= x <= max(one, two)
        for one, two in borders_1d
    )

    return on_edge

def line_inside_polygon(
    borders: List[Tuple[Tile, Tile]],
    a: Tile,
    b: Tile
) -> bool:
    """ Returns true if the rectangle defined by (a, b) is entirely contained
    within the polygon defined by the borders (inclusive) """

    if a.x == b.x:
        perpendicular_1d = [
            one.y for one, two in borders
            if min(one.x, two.x) <= a.x < max(one.x, two.x)
            and one.y == two.y
        ]
        parallel_1d = [
            (min(one.y, two.y), max(one.y, two.y)) for one, two in borders
            if one.x == two.x == a.x
        ]

        return all(
            point_inside_polygon_1d(perpendicular_1d, y) or point_on_edge_1d(parallel_1d, y)
            for y in range(a.y, b.y + 1)
        )
    elif a.y == b.y:
        perpendicular_1d = [
            one.x for one, two in borders
            if min(one.y, two.y) <= a.y < max(one.y, two.y)
            and one.x == two.x
        ]
        parallel_1d = [
            (min(one.x, two.x), max(one.x, two.x))
            for one, two in borders
            if one.y == two.y == a.y
        ]

        return all(
            point_inside_polygon_1d(perpendicular_1d, x) or point_on_edge_1d(parallel_1d, x)
            for x in range(a.x, b.x + 1)
        )
    else:
        raise ValueError("only horizontal or vertical lines are supported")

def rectangle_inside(
    borders: List[Tuple[Tile, Tile]],
    a: Tile,
    b: Tile
) -> bool:
    min_x, max_x = min(a.x, b.x), max(a.x, b.x)
    min_y, max_y = min(a.y, b.y), max(a.y, b.y)

    if not line_inside_polygon(borders, Tile(min_x, min_y), Tile(min_x, max_y)):
        return False
    if not line_inside_polygon(borders, Tile(min_x, max_y), Tile(max_x, max_y)):
        return False
    if not line_inside_polygon(borders, Tile(max_x, min_y), Tile(max_x, max_y)):
        return False
    if not line_inside_polygon(borders, Tile(min_x, min_y), Tile(max_x, min_y)):
        return False
    return True

def rectangle_area(a: Tile, b: Tile) -> int:
    return (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)

def main() -> int:
    tiles = parse_tiles(stdin)
    rectangles, green_borders = build_every_rectangle(tiles), build_green_borders(tiles)

    print(max(rectangle_area(a, b) for a, b in rectangles)) # 4758121828
    print(max(rectangle_area(a, b) for a, b in rectangles if rectangle_inside(green_borders, a, b))) # 1577956170

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

        assert max(rectangle_area(a, b) for a, b in rectangles if rectangle_inside(green_borders, a, b)) == 24
