def parse_memory(text):
    memory = {}

    for item in text.split(","):
        tag, value = item.split("=")
        memory[tag.strip()] = int(value.strip())

    return memory

def parse_operation(line):
    processor, instruction = line.split(":", 1)

    processor = processor.strip()
    instruction = instruction.strip()

    operation, arguments = instruction.split("(", 1)

    if not arguments.endswith(")"):
        raise ValueError("Invalid operation format")

    arguments = arguments[:-1]
    arguments = arguments.split(",")

    operation = operation.strip()
    tag = arguments[0].strip()
    value = None

    if operation == "Write" and len(arguments) == 2:
        value = int(arguments[1].strip())

    elif operation in ("Read", "Replace") and len(arguments) == 1:
        pass

    else:
        raise ValueError(f"Invalid operation: {instruction}")

    return {
        "processor": processor,
        "operation": operation,
        "tag": tag,
        "value": value
    }

def parse_input(filename):
    with open(filename, "r") as file:
        lines = [
            line.strip()
            for line in file
            if line.strip() and not line.strip().startswith("#")
        ]

    if len(lines) < 3:
        raise ValueError("Missing input configuration")

    protocol = lines[0].split(":", 1)[1].strip()

    memory_text = lines[1].split(":", 1)[1].strip()
    memory = parse_memory(memory_text)

    processors_text = lines[2].split(":", 1)[1].strip()
    processors = [
        p.strip() for p in processors_text.split(",")
    ]

    operations = []

    for line in lines[3:]:
        operations.append(parse_operation(line))

        validate_input(protocol, memory, processors, operations)

    return protocol, memory, processors, operations


def validate_input(protocol, memory, processors, operations):
    supported_protocols = [
        "WRITE_INVALIDATE_WRITE_THROUGH",
        "WRITE_INVALIDATE_WRITE_BACK",
        "WRITE_ONCE"
    ]

    if protocol not in supported_protocols:
        raise ValueError("Unsupported coherence protocol")

    if not 1 <= len(memory) <= 3:
        raise ValueError("Memory must contain 1 to 3 variables")

    if not 1 <= len(processors) <= 3:
        raise ValueError("There must be 1 to 3 processors")

    if len(set(processors)) != len(processors):
        raise ValueError("Duplicate processor IDs")

    for operation in operations:

        if operation["processor"] not in processors:
            raise ValueError("Unknown processor")

        if operation["tag"] not in memory:
            raise ValueError("Unknown memory variable")


