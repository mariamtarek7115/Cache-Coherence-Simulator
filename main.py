from cache import Cache
from memory import MainMemory
from bus import SharedBus
from protocols import WriteOnce

memory = MainMemory({"X": 5})

caches = {
    "P": Cache("P"),
    "Q": Cache("Q")
}

bus = SharedBus(memory, caches)
protocol = WriteOnce(bus)

def show_state(event):
    print("\nEvent:", event)
    print("Memory:", memory.get_all())

    for processor_id, cache in caches.items():
        block = cache.get_block("X")

        if block is None:
            print(processor_id, "-", "-")
        else:
            print(processor_id, block.value, block.state.value)


show_state("Initial State")

show_state(protocol.read(caches["P"], "X"))

show_state(protocol.read(caches["Q"], "X"))

show_state(protocol.write(caches["Q"], "X", 10))

show_state(protocol.read(caches["Q"], "X"))

show_state(protocol.write(caches["Q"], "X", 15))

show_state(protocol.write(caches["P"], "X", 20))

show_state(protocol.read(caches["Q"], "X"))

