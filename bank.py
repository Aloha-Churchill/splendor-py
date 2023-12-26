from gemstone import Gemstone, GemstoneType

class Bank:
    def __init__(self):
        self.gemstones = {gemstone_type: Gemstone(gemstone_type, 5) for gemstone_type in GemstoneType}

    def add_gemstones(self, gemstone_type: GemstoneType, quantity: int):
        self.gemstones[gemstone_type].add(quantity)

    def remove_gemstones(self, gemstone_type: GemstoneType, quantity: int):
        self.gemstones[gemstone_type].remove(quantity)

    def __str__(self) -> str:
        return '\n'.join(str(gemstone) for gemstone in self.gemstones.values())
    
    def can_remove_gemstones(self, gemstone_type: GemstoneType, quantity: int) -> bool:
        return self.gemstones[gemstone_type].quantity >= quantity