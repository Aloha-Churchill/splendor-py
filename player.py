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

    def draw_token(self, gemstone: GemstoneType, amount: int = 1):
        """
        Method for a player to draw tokens.
        """
        self.tokens[gemstone] += amount

    def purchase_card(self, card: Card):
        if self.can_purchase(card):
            # Deduct the cost from the player's tokens
            for gemstone, cost in card.cost.items():
                self.tokens[gemstone] -= cost
            # Add the card to the player's hand
            self.resource_cards.append(card)
            self.points += card.points
        else:
            raise ValueError("Not enough tokens to purchase the card")
        
    def can_acquire_noble(self, noble):
        """
        Check if the player has enough bonuses to acquire the noble.
        """
        player_bonuses = self.total_bonus()
        return all(player_bonuses.get(gemstone, 0) >= required_amount for gemstone, required_amount in noble.cost.items())
    
    def total_bonus(self):
        """
        Calculate the total bonus gems the player has from their resource cards.
        """
        bonuses = {gemstone: 0 for gemstone in GemstoneType}
        for card in self.resource_cards:
            bonuses[card.bonus] += 1
        return bonuses

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
