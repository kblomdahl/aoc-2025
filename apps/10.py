from dataclasses import dataclass
from sys import exit, stdin, maxsize
from typing import List
from re import fullmatch

@dataclass(frozen=True, slots=True)
class Machine:
    light_diagram: str
    buttons: List[List[int]]
    voltage_requirements: List[int]
    min_presses: int = 0

def parse_machine(line: str) -> Machine:
    light_diagram = ""
    buttons = []
    voltage_requirements = []

    for part in line.split():
        if fullmatch(r"\[[\.#]+\]", part):
            light_diagram = part.strip("[]")
        elif fullmatch(r"\(\d+(,\d+)*\)", part):
            buttons.append(list(map(int, part.strip("()").split(","))))
        elif fullmatch(r"\{\d+(,\d+)*\}", part):
            voltage_requirements = list(map(int, part.strip("{}").split(",")))
        else:
            raise ValueError(f"Invalid machine instruction: {part}")

    return Machine(light_diagram, buttons, voltage_requirements)

def minimum_button_presses(machine: Machine, voltage: bool = False) -> int:
    from z3 import Int, Optimize, Sum, sat # type: ignore
    from typing import Any

    solver = Optimize()
    button_exprs = [list[Any]() for _ in range(len(machine.voltage_requirements))]
    button_vars = [Int(f"button[{i}]") for i in range(len(machine.buttons))]

    for i, button_var in enumerate(button_vars):
        for j in machine.buttons[i]:
            button_exprs[j].append(button_var)

        solver.add(button_var >= 0)

    if voltage:
        for i, voltage_requirement in enumerate(machine.voltage_requirements):
            solver.add(Sum(button_exprs[i]) == voltage_requirement)
    else:
        for i, light in enumerate(machine.light_diagram):
            if light == "#":
                solver.add(Sum(button_exprs[i]) % 2 == 1)
            else:
                solver.add(Sum(button_exprs[i]) % 2 == 0)

    objective = solver.minimize(Sum(button_vars))

    if solver.check() != sat:
        return maxsize
    return solver.lower(objective).as_long() # type: ignore

def main() -> int:
    machines = [parse_machine(line.strip()) for line in stdin if line.strip()]

    print(sum(minimum_button_presses(machine) for machine in machines))
    print(sum(minimum_button_presses(machine, voltage=True) for machine in machines))

    return 0

if __name__ == "__main__":
    exit(main())

# -------- Tests --------

from pytest import fixture

class Test:
    @fixture
    def machines(self) -> List[Machine]:
        lines = """
            [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
            [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
        """.strip().splitlines()

        return list(map(lambda line: parse_machine(line.strip()), lines))

    def test_example_1(self, machines: List[Machine]) -> None:
        assert sum(minimum_button_presses(machine) for machine in machines) == 7

    def test_example_2(self, machines: List[Machine]) -> None:
        assert sum(minimum_button_presses(machine, voltage=True) for machine in machines) == 33
