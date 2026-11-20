from parser import parse_input

protocol, memory, processors, operations = parse_input("input.txt")

print("Protocol:", protocol)
print("Memory:", memory)
print("Processors:", processors)

print("\nOperations:")

for operation in operations:
    print(operation)