from cache import Cache
from memory import MainMemory
from bus import SharedBus

from protocols import (
    WriteInvalidateWriteThrough,
    WriteInvalidateWriteBack,
    WriteOnce
)


class CoherenceSimulator:
    def __init__(self, protocol_name, memory, processors, operations):

        self.protocol_name = protocol_name

        self.memory = MainMemory(memory)

        self.caches = {
            processor: Cache(processor)
            for processor in processors
        }

        self.bus = SharedBus(self.memory, self.caches)

        self.operations = operations
        self.variables = list(memory.keys())
        self.processors = processors

        self.stats = {
            "Read-Hit": 0,
            "Read-Miss": 0,
            "Write-Hit": 0,
            "Write-Miss": 0,
            "Replacement": 0
        }

        self.trace = []

        protocols = {
            "WRITE_INVALIDATE_WRITE_THROUGH":
                WriteInvalidateWriteThrough,

            "WRITE_INVALIDATE_WRITE_BACK":
                WriteInvalidateWriteBack,

            "WRITE_ONCE":
                WriteOnce
        }

        self.protocol = protocols[protocol_name](self.bus)

    def record_state(self, serial, event):

        row = [serial, event]

        # Record global memory values
        for tag in self.variables:
            row.append(self.memory.read(tag))

        # Record each processor's cache
        for processor in self.processors:

            cache = self.caches[processor]

            for tag in self.variables:

                block = cache.get_block(tag)

                if block is None:
                    row.extend(["-", "-"])

                else:
                    row.extend([
                        block.value,
                        block.state.value
                    ])

        self.trace.append(row)

    def step(self, serial, operation):

        processor = operation["processor"]
        action = operation["operation"]
        tag = operation["tag"]
        value = operation["value"]

        cache = self.caches[processor]

        if action == "Read":

            result = self.protocol.read(cache, tag)

            event = f"{processor} reads {tag} ({result})"

        elif action == "Write":

            result = self.protocol.write(cache, tag, value)

            event = (
                f"{processor} writes {tag}={value} "
                f"({result})"
            )

        elif action == "Replace":

            result = self.protocol.replace(cache, tag)

            event = f"{processor} replaces {tag} ({result})"

        else:
            raise ValueError(f"Unknown operation: {action}")

        self.stats[result] += 1

        self.record_state(serial, event)

    def run_all(self):

        self.record_state(0, "Initial State")

        for serial, operation in enumerate(
            self.operations, start=1
        ):
            self.step(serial, operation)

    def print_table(self, headers, rows):

        widths = [
            len(str(header))
            for header in headers
        ]

        for row in rows:
            for i, item in enumerate(row):
                widths[i] = max(
                    widths[i], len(str(item))
                )

        def format_row(row):
            return " | ".join(
                str(item).ljust(widths[i])
                for i, item in enumerate(row)
            )

        separator = "-+-".join(
            "-" * width for width in widths
        )

        print(separator)
        print(format_row(headers))
        print(separator)

        for row in rows:
            print(format_row(row))

        print(separator)

    def print_trace_table(self):

        headers = ["Serial", "Event"]

        for tag in self.variables:
            headers.append(f"Mem({tag})")

        for processor in self.processors:

            for tag in self.variables:

                headers.append(f"{processor} Val({tag})")
                headers.append(f"{processor} State({tag})")

        print("\nOPERATION TRACE TABLE")
        print("Protocol:", self.protocol_name)

        self.print_table(headers, self.trace)

    def print_summary(self):

        print("\nFINAL SYSTEM STATE")

        headers = ["Variable", "Memory"]

        for processor in self.processors:
            headers.extend([
                f"{processor} Value",
                f"{processor} State"
            ])

        rows = []

        for tag in self.variables:

            row = [tag, self.memory.read(tag)]

            for processor in self.processors:

                block = self.caches[processor].get_block(tag)

                if block is None:
                    row.extend(["-", "-"])

                else:
                    row.extend([
                        block.value,
                        block.state.value
                    ])

            rows.append(row)

        self.print_table(headers, rows)

        print("\nEXECUTION STATISTICS")

        for event, count in self.stats.items():
            print(f"{event}: {count}")

        print(
            "Bus Invalidation Commands:",
            self.bus.invalidation_count
        )

        print(
            "Update Broadcasts:",
            self.bus.update_count
        )

        print(
            "Memory Write-Back Operations:",
            self.bus.write_back_count
        )