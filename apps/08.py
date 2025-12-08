from array import array
from dataclasses import dataclass
from sys import exit, stdin
from typing import List, TextIO, Tuple
from math import prod
from io import StringIO
from heapq import nsmallest, nlargest, heapify, heappop
from itertools import combinations

@dataclass(frozen=True, slots=True)
class JunctionBox:
    x: int
    y: int
    z: int

def parse_junction_boxes(lines: TextIO) -> List[JunctionBox]:
    return [JunctionBox(*map(int, line.strip().split(","))) for line in lines if line.strip()]

def build_every_edge(boxes: List[JunctionBox]) -> List[Tuple[int, int, int]]:
    return [
        ((boxes[i].x - boxes[j].x) ** 2 + (boxes[i].y - boxes[j].y) ** 2 + (boxes[i].z - boxes[j].z) ** 2, i, j)
        for i, j in combinations(range(len(boxes)), 2)
    ]

def merge_sets(parents: array[int], sizes: array[int], a: int, b: int) -> int | None:
    def find_set_root(x: int) -> int:
        while x != parents[x]:
            x, parents[x] = parents[x], parents[parents[x]]
        return x

    root_a, root_b = find_set_root(a), find_set_root(b)

    if root_a == root_b:
        return None
    if sizes[root_a] < sizes[root_b]:
        root_a, root_b = root_b, root_a

    parents[root_b] = root_a
    sizes[root_a] += sizes[root_b]

    return root_a

def largest_clusters(
    edges: List[Tuple[int, int, int]],
    n: int,
    k: int = 3
) -> List[int]:
    parents, sizes = array('i', range(n)), array('i', [1] * n)

    for _, a, b in edges:
        merge_sets(parents, sizes, a, b)

    return nlargest(k, [sz for i, sz in enumerate(sizes) if parents[i] == i])

def min_k_cluster(
    edges: List[Tuple[int, int, int]],
    n: int,
    k: int = 1000
) -> Tuple[int, int]:
    parents, sizes = array('i', range(n)), array('i', [1] * n)

    heapify(edges)
    while edges:
        _, a, b = heappop(edges)

        if root := merge_sets(parents, sizes, a, b):
            if sizes[root] >= k:
                return a, b

    raise ValueError("disconnected graph")

def main() -> int:
    junction_boxes = list(parse_junction_boxes(stdin))
    edges, n = build_every_edge(junction_boxes), len(junction_boxes)

    print(prod(largest_clusters(nsmallest(1000, edges), n)))
    print(prod(junction_boxes[i].x for i in min_k_cluster(edges, n, k=n)))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def junction_boxes(self) -> List[JunctionBox]:
        content = """
            162,817,812
            57,618,57
            906,360,560
            592,479,940
            352,342,300
            466,668,158
            542,29,236
            431,825,988
            739,650,466
            52,470,668
            216,146,977
            819,987,18
            117,168,530
            805,96,715
            346,949,466
            970,615,88
            941,993,340
            862,61,35
            984,92,344
            425,690,689
        """

        return list(parse_junction_boxes(StringIO(content)))

    def test_example_1(self, junction_boxes: List[JunctionBox]) -> None:
        edges, n = build_every_edge(junction_boxes), len(junction_boxes)

        assert prod(largest_clusters(nsmallest(10, edges), n)) == 40

    def test_example_2(self, junction_boxes: List[JunctionBox]) -> None:
        edges, n = build_every_edge(junction_boxes), len(junction_boxes)

        assert prod(junction_boxes[i].x for i in min_k_cluster(edges, n, k=n)) == 25272
