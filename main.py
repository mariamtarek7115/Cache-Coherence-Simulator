from cache import Cache, CacheState

cache = Cache("P1")

# Initially empty
print(cache.has_valid_block("X"))

# Insert a block
cache.set_block("X", 5, CacheState.RO)

print(cache.has_valid_block("X"))
print(cache.get_block("X").value)
print(cache.get_block("X").state.value)

# Invalidate the block
cache.invalidate("X")

print(cache.has_valid_block("X"))
print(cache.get_block("X").state.value)

# Remove the block
cache.remove_block("X")

print(cache.get_block("X"))