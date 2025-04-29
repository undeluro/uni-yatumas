from yatumas.machine.machine import Machine
from yatumas.machine.symbol import Symbol
from yatumas.parser.parser import parse_input, parse_machine
from yatumas.simulator.simulation import GraphicalSimulation
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from pathlib import Path


def simulate(
    machine: Machine, machine_input: list[Symbol], step_interval_in_sec: float = 10
) -> None:
    graphical_simulation = GraphicalSimulation(
        machine, machine_input, step_interval_in_sec
    )
    graphical_simulation.run()


def create_arg_parser() -> ArgumentParser:
    """
    Creates an ArgumentParses responsible for parsing the command line arguments.
    """

    arg_parser = ArgumentParser(
        "Yet Another Turing Machine Simulator",
        formatter_class=ArgumentDefaultsHelpFormatter,  # displays the default values in help: https://docs.python.org/3/library/argparse.html#argparse.ArgumentDefaultsHelpFormatter
        description="An exciting interpreter for a Turing Complete programming language also known as a Turing Machine.",
    )

    arg_parser.add_argument(
        "--machine",
        "-m",
        required=True,
        type=Path,
        help="Path to a file containing the Turing Machine definition. It's a required argument.",
    )
    arg_parser.add_argument(
        "--interval",
        "-i",
        type=float,
        default=0.3,
        help="Time interval (in seconds) between the simulation steps in the (default) graphical mode.",
    )
    arg_parser.add_argument(
        "input", type=str, help="an input used to initialize the machine tape"
    )
    return arg_parser


def build_machine(filepath: Path) -> Machine:
    with open(filepath) as f:
        return parse_machine(f.readlines())


def main():
    """
    Entry point of the script when run from the command line.
    It sets up the simulation environment based on user-provided arguments and starts the simulation.
    """
    arg_parser = create_arg_parser()
    args = arg_parser.parse_args()
    machine = build_machine(args.machine)
    machine_input = parse_input(args.input)
    simulate(machine, machine_input, args.interval)


if __name__ == "__main__":
    main()
