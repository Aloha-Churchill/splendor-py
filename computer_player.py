from player import Player
import random
from gemstone import GemstoneType

class ComputerPlayer(Player):
    
    def take_turn(self, game):
        actions = [self.draw_3_unique_gems, self.draw_2_same_gems, self.purchase_card, self.reserve_card]
        actions = [action for action in actions if self.can_perform_action(action, game)]
        if actions:
            action = random.choice(actions)
            action_message = action(game)
            return action_message

    def can_perform_action(self, action, game):
        if action == self.draw_3_unique_gems:
            return game.bank.has_sufficient_gems_for_3_unique_gems()
        elif action == self.draw_2_same_gems:
            return game.bank.has_sufficient_gems_for_2_same_gems()
        elif action == self.purchase_card:
            return any(self.can_purchase(card) for row in game.card_rows for card in row)
        elif action == self.purchase_reserved_card:
            return any(self.can_purchase(card) for card in self.reserved_cards)
        elif action == self.reserve_card:
            return any(len(row) > 0 for row in game.card_rows)
        return False

    def draw_3_unique_gems(self, game):
        # Exclude GOLD from the selection
        gemstones = random.sample([gt for gt in GemstoneType if gt != GemstoneType.GOLD and game.bank.gemstones[gt].quantity >= 1], 3)
        for gemstone in gemstones:
            self.tokens[gemstone] += 1
            game.bank.gemstones[gemstone].quantity -= 1
        gemstone_names = ', '.join([gt.value for gt in gemstones])
        return f"Drew 3 unique gems: {gemstone_names}"

    def draw_2_same_gems(self, game):
        # Exclude GOLD from the selection and check for sufficient quantity
        gemstone_options = [gt for gt in GemstoneType if gt != GemstoneType.GOLD and game.bank.gemstones[gt].quantity >= 6]
        if gemstone_options:
            gemstone = random.choice(gemstone_options)
            self.tokens[gemstone] += 2
            game.bank.gemstones[gemstone].quantity -= 2
            return f"Drew 2 {gemstone.value} gems"
        return "No action taken"

    def purchase_card(self, game):
        purchasable_cards = [card for row in game.card_rows for card in row if self.can_purchase(card)]
        if purchasable_cards:
            card = random.choice(purchasable_cards)
            super().purchase_card(card)  # Call parent class's purchase_card method
            game.remove_card_from_row(card)
            return f"Purchased a card with {card.points} points"

    def reserve_card(self, game):
        reservable_cards = [card for deck in [game.card_deck_l1, game.card_deck_l2, game.card_deck_l3] for card in deck.items]
        if reservable_cards:
            card = random.choice(reservable_cards)
            super().reserve_card(card, game.bank)  # Pass the bank as an argument
            game.remove_card_from_row(card)
            return "Reserved a card"
        return "No action taken"
    
    def purchase_reserved_card(self, game):
        if self.reserved_cards:
            card = random.choice(self.reserved_cards)
            if self.can_purchase(card):
                super().purchase_card(card)
                self.reserved_cards.remove(card)
                return f"Purchased a reserved card with {card.points} points"
        return "No action taken"
