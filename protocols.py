from cache import CacheState


class WriteInvalidateWriteThrough:
    def __init__(self, bus):
        self.bus = bus

    def read(self, cache, tag):

        # Read-Hit
        if cache.has_valid_block(tag):
            return "Read-Hit"

        # Read-Miss
        self.bus.broadcast_read(tag, cache.processor_id)
        value = self.bus.read_from_memory(tag)

        cache.set_block(tag, value, CacheState.VALID)

        return "Read-Miss"

    def write(self, cache, tag, value):

        if cache.has_valid_block(tag):
            event = "Write-Hit"

        else:
            event = "Write-Miss"

            self.bus.broadcast_read(tag, cache.processor_id)
            old_value = self.bus.read_from_memory(tag)

            cache.set_block(tag, old_value, CacheState.VALID)

        # Invalidate other caches
        self.bus.broadcast_invalidate(tag, cache.processor_id)

        # Update global memory
        self.bus.write_through(tag, value)

        # Update local cache
        cache.set_block(tag, value, CacheState.VALID)

        return event

    def replace(self, cache, tag):

        cache.remove_block(tag)

        return "Replacement"