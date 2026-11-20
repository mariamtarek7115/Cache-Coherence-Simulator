import sys

from parser import parse_input
from simulator import CoherenceSimulator


def main():

    filename = (
        sys.argv[1] if len(sys.argv) > 1
        else "input.txt"
    )

    try:

        protocol, memory, processors, operations = (
            parse_input(filename)
        )

        simulator = CoherenceSimulator(
            protocol,
            memory,
            processors,
            operations
        )

        simulator.run_all()

        simulator.print_trace_table()

        simulator.print_summary()

    except (OSError, ValueError) as error:

        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()