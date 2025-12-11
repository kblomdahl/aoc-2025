from sys import exit, stdin
from typing import Dict, List, TextIO
from io import StringIO
from functools import cache

def parse_devices(input: TextIO) -> dict[str, List[str]]:
    return {
        line.strip().split(":")[0]: line.strip().split(":")[1].split()
        for line in input
        if line.strip()
    }

def find_all_paths(
    devices: dict[str, List[str]],
    start: str,
    end: str
) -> int:
    @cache
    def dfs(current: str) -> int:
        if current == end:
            return 1
        return sum(dfs(neighbour) for neighbour in devices.get(current, []))

    return dfs(start)

def find_all_paths_that_visit(
    devices: Dict[str, List[str]],
    start: str,
    end: str,
    visit: List[str]
) -> int:
    if not visit:
        return find_all_paths(devices, start, end)

    total_paths = 0

    for device in visit:
        path_to_device = find_all_paths(devices, start, device)
        path_to_end = find_all_paths_that_visit(devices, device, end, [d for d in visit if d != device])
        total_paths += path_to_device * path_to_end

    return total_paths

def main() -> int:
    devices = parse_devices(stdin)

    print(find_all_paths(devices, "you", "out"))
    print(find_all_paths_that_visit(devices, "svr", "out", ["dac", "fft"]))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def devices_1(self) -> dict[str, List[str]]:
        content = """
            aaa: you hhh
            you: bbb ccc
            bbb: ddd eee
            ccc: ddd eee fff
            ddd: ggg
            eee: out
            fff: out
            ggg: out
            hhh: ccc fff iii
            iii: out
        """

        return parse_devices(StringIO(content.strip()))

    @fixture
    def devices_2(self) -> dict[str, List[str]]:
        content = """
            svr: aaa bbb
            aaa: fft
            fft: ccc
            bbb: tty
            tty: ccc
            ccc: ddd eee
            ddd: hub
            hub: fff
            eee: dac
            dac: fff
            fff: ggg hhh
            ggg: out
            hhh: out
        """

        return parse_devices(StringIO(content.strip()))

    def test_example_1(self, devices_1: dict[str, List[str]]) -> None:
        assert find_all_paths(devices_1, "you", "out") == 5

    def test_example_2(self, devices_2: dict[str, List[str]]) -> None:
        assert find_all_paths_that_visit(devices_2, "svr", "out", ["dac", "fft"]) == 2
