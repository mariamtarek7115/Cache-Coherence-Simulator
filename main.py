from cache import Cache, CacheState
from memory import MainMemory
from bus import SharedBus

# Initialize main memory
memory = MainMemory({"X": 5, "Y": 10, "Z": 20})

# Initialize processor caches
caches = {
    "P1": Cache("P1"),
    "P2": Cache("P2"),
    "P3": Cache("P3")
}

# Initialize shared bus
bus = SharedBus(memory, caches)

# Test 1: Read from memory
print("Memory X:", bus.read_from_memory("X"))

# Test 2: Store X in all caches
for cache in caches.values():
    cache.set_block("X", 5, CacheState.VALID)

# Test 3: Broadcast read
remote_blocks = bus.broadcast_read("X", "P1")
print("Remote valid copies:", len(remote_blocks))

# Test 4: P1 broadcasts invalidation
bus.broadcast_invalidate("X", "P1")

for processor_id, cache in caches.items():
    print(processor_id, cache.get_block("X").state.value)

# Test 5: Write-through
bus.write_through("X", 10)
print("After write-through:", memory.get_all())

# Test 6: Write-back
bus.write_back_to_memory("X", 20)
print("After write-back:", memory.get_all())

# Test 7: Statistics
print("Invalidation commands:", bus.invalidation_count)
print("Write-backs:", bus.write_back_count)