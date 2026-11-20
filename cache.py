from enum import Enum

class CacheState(Enum):
    INV = "INV"
    VALID = "VALID"
    RO = "RO"
    RW = "RW"
    RES = "RES"
    DIRTY = "DIRTY"

class CacheBlock:
    def __init__(self, tag, value, state):
        self.tag = tag
        self.value = value
        self.state = state

    def is_valid(self):
        return self.state != CacheState.INV

class Cache:
    def __init__(self, processor_id):
        self.processor_id = processor_id
        self.blocks = {}

    def get_block(self, tag):
        return self.blocks.get(tag)

    def has_valid_block(self, tag):
        block = self.get_block(tag)
        return block is not None and block.is_valid()

    def set_block(self, tag, value, state):
        self.blocks[tag] = CacheBlock(tag, value, state)

    def invalidate(self, tag):
        block = self.get_block(tag)

        if block is not None:
            block.state = CacheState.INV

    def remove_block(self, tag):
        self.blocks.pop(tag, None)