from enum import Enum
from dataclasses import dataclass

class GemstoneType(Enum):
    DIAMOND = "Diamond"
    EMERALD = "Emerald"
    RUBY = "Ruby"
    SAPPHIRE = "Sapphire"
    ONYX = "Onyx"
    GOLD = "Gold"

@dataclass
class Gemstone:
    type: GemstoneType
    quantity: int = 0

    def add(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot add a negative amount of gemstones")
        self.quantity += amount

    def remove(self, amount: int) -> None:
        if amount < 0:
            raise ValueError("Cannot remove a negative amount of gemstones")
        if amount > self.quantity:
            raise ValueError(f"Not enough {self.type.value} gemstones to remove")
        self.quantity -= amount

    def __str__(self) -> str:
        return f"{self.type.value} gemstone: {self.quantity}"
