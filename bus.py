class SharedBus:
    def __init__(self, memory, caches):
        self.memory = memory
        self.caches = caches

        self.invalidation_count = 0
        self.write_back_count = 0
        self.update_count = 0

    def broadcast_read(self, tag, requester_id):
        remote_blocks = []

        for processor_id, cache in self.caches.items():
            if processor_id != requester_id:
                if cache.has_valid_block(tag):
                    remote_blocks.append(cache.get_block(tag))

        return remote_blocks

    def broadcast_invalidate(self, tag, sender_id):
        self.invalidation_count += 1

        for processor_id, cache in self.caches.items():
            if processor_id != sender_id:
                cache.invalidate(tag)

    def read_from_memory(self, tag):
        return self.memory.read(tag)

    def write_through(self, tag, value):
        self.memory.write(tag, value)

    def write_back_to_memory(self, tag, value):
        self.memory.write(tag, value)
        self.write_back_count += 1