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
    
    def has_sufficient_gems_for_draw(self):
        # Check if there are at least two gems of the same type
        if any(gemstone.quantity >= 2 for gemstone in self.gemstones.values()):
            return True
        # Check if there are at least three types of gems with at least one available
        if sum(gemstone.quantity >= 1 for gemstone in self.gemstones.values()) >= 3:
            return True
        
        return False

    # has sufficient gems for 3_unique_gems
    def has_sufficient_gems_for_3_unique_gems(self):
        return sum(gemstone.quantity >= 1 for gemstone in self.gemstones.values()) >= 3
    
    # has sufficient gems for 2_same_gems
    def has_sufficient_gems_for_2_same_gems(self):
        return any(gemstone.quantity >= 6 for gemstone in self.gemstones.values())