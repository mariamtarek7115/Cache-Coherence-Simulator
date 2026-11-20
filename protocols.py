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

class WriteInvalidateWriteBack:
    def __init__(self, bus):
        self.bus = bus

    def find_owner(self, cache, tag):

        remote_blocks = self.bus.broadcast_read(
            tag, cache.processor_id
        )

        for block in remote_blocks:
            if block.state == CacheState.RW:
                return block

        return None

    def read(self, cache, tag):

        # Read-Hit
        if cache.has_valid_block(tag):
            return "Read-Hit"

        # Read-Miss
        owner = self.find_owner(cache, tag)

        if owner is not None:
            value = owner.value

            self.bus.write_back_to_memory(tag, value)

            owner.state = CacheState.RO

        else:
            value = self.bus.read_from_memory(tag)

        cache.set_block(tag, value, CacheState.RO)

        return "Read-Miss"

    def write(self, cache, tag, value):

        if cache.has_valid_block(tag):

            block = cache.get_block(tag)

            # Write-Hit in RW
            if block.state == CacheState.RW:
                block.value = value
                return "Write-Hit"

            # Write-Hit in RO
            event = "Write-Hit"

        else:
            # Write-Miss
            event = "Write-Miss"

            owner = self.find_owner(cache, tag)

            if owner is not None:
                old_value = owner.value

            else:
                old_value = self.bus.read_from_memory(tag)

            cache.set_block(tag, old_value, CacheState.RO)

        # Invalidate other caches
        self.bus.broadcast_invalidate(
            tag, cache.processor_id
        )

        # Become the new exclusive owner
        cache.set_block(tag, value, CacheState.RW)

        return event

    def replace(self, cache, tag):

        block = cache.get_block(tag)

        if block is not None:
            if block.state == CacheState.RW:
                self.bus.write_back_to_memory(
                    tag, block.value
                )

            cache.remove_block(tag)

        return "Replacement"