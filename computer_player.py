from player import Player
import random
from gemstone import GemstoneType

class ComputerPlayer(Player):
    def take_turn(self, game):
        actions = [self.draw_gems, self.purchase_card, self.reserve_card, self.purchase_reserved_card]
        actions = [action for action in actions if self.can_perform_action(action, game)]
        if actions:
            action = random.choice(actions)
            action_message = action(game)
            return action_message

    def can_perform_action(self, action, game):
        if action == self.draw_gems:
            return game.bank.has_sufficient_gems_for_draw()
        elif action == self.purchase_card or action == self.purchase_reserved_card:
            return True
        elif action == self.reserve_card:
            return any(len(row) > 0 for row in game.card_rows)
        return False

    def draw_gems(self, game):
        if random.choice([True, False]):
            gemstone = random.choice([gt for gt in GemstoneType if game.bank.gemstones[gt].quantity >= 2])
            self.tokens[gemstone] += 2
            game.bank.gemstones[gemstone].quantity -= 2
            return f"Drew 2 {gemstone.value} gems"
        else:
            gemstones = random.sample([gt for gt in GemstoneType if game.bank.gemstones[gt].quantity >= 1], 3)
            for gemstone in gemstones:
                self.tokens[gemstone] += 1
                game.bank.gemstones[gemstone].quantity -= 1
            gemstone_names = ', '.join([gt.value for gt in gemstones])
            return f"Drew 3 unique gems: {gemstone_names}"

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
            if game.bank.gemstones[GemstoneType.GOLD].quantity > 0:
                self.tokens[GemstoneType.GOLD] += 1
                game.bank.gemstones[GemstoneType.GOLD].quantity -= 1
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
