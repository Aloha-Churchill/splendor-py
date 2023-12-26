from dataclasses import dataclass, field
from typing import Dict, List
from gemstone import GemstoneType
from card import Card
from bank import Bank

@dataclass
class Player:
    name: str
    tokens: Dict[GemstoneType, int] = field(default_factory=lambda: {gemstone: 0 for gemstone in GemstoneType})
    points: int = 0
    resource_cards: List[Card] = field(default_factory=list)
    reserved_cards: List[Card] = field(default_factory=list)

    def draw_token(self, gemstone: GemstoneType, amount: int = 1):
        """
        Method for a player to draw tokens.
        """
        self.tokens[gemstone] += amount

    def purchase_card(self, card: Card):
        """
        Method for a player to purchase a card.
        This method should include logic to check if the player
        has enough tokens and then deduct the cost from the player's tokens.
        """
        # Example check (to be expanded based on game rules)
        if all(self.tokens[gemstone] >= cost for gemstone, cost in card.cost.items()):
            self.resource_cards.append(card)
            for gemstone, cost in card.cost.items():
                self.tokens[gemstone] -= cost
            self.points += card.points
        else:
            raise ValueError("Not enough tokens to purchase the card")

    def reserve_card(self, card: Card, bank: Bank):
        self.reserved_cards.append(card)
        if bank.can_remove_gemstones(GemstoneType.GOLD, 1):
            self.tokens[GemstoneType.GOLD] += 1
            bank.remove_gemstones(GemstoneType.GOLD, 1)

    def total_bonus(self) -> Dict[GemstoneType, int]:
        """
        Calculate the total bonus gems the player has from their resource cards.
        """
        bonus = {gemstone: 0 for gemstone in GemstoneType}
        for card in self.resource_cards:
            bonus[card.bonus] += 1
        return bonus

    def __str__(self) -> str:
        tokens_str = ', '.join(f"{gemstone.value}: {amount}" for gemstone, amount in self.tokens.items())
        return f"Player: {self.name}, Tokens: [{tokens_str}], Points: {self.points}"


    def can_purchase(self, card: Card) -> bool:
        # Check if the player can afford the card
        for gemstone, cost in card.cost.items():
            if self.tokens[gemstone] < cost:
                return False
        return True
    
    def can_draw_gemstone(self, gemstone_type: GemstoneType, bank: Bank) -> bool:
        """
        Check if the player can draw a specific type of gemstone from the bank.
        Implement the logic according to the game rules.
        """
        # Example: Check if the bank has enough of the gemstone
        return bank.can_remove_gemstones(gemstone_type, 1)
