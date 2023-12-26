from dataclasses import dataclass
from gemstone import GemstoneType

@dataclass
class Card:
    level: int
    cost: dict[GemstoneType, int]
    bonus: GemstoneType
    points: int = 0

    def __str__(self) -> str:
        cost_str = ', '.join(f"{gemstone_type.value}: {amount}" for gemstone_type, amount in self.cost.items())
        return f"Level: {self.level}, Cost: [{cost_str}], Bonus: {self.bonus.value}, Points: {self.points}"

@dataclass
class Noble:
    cost: dict[GemstoneType, int]
    points: int

    def __str__(self) -> str:
        cost_str = ', '.join(f"{gemstone_type.value}: {amount}" for gemstone_type, amount in self.cost.items())
        return f"Requirements: [{cost_str}], Points: {self.points}"
