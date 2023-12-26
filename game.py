from deck import Deck, initialize_decks_from_csv
from bank import Bank
from display import display_board, get_player_names
from player import Player
from typing import List


class Game:
    def __init__(self, players: List[Player]):
        # get initial game state
        self.players = players
        self.bank = Bank()
        self.card_deck_l1, self.card_deck_l2, self.card_deck_l3, self.noble_deck = initialize_decks_from_csv('./cards.csv')
        self.current_player_index = 0

        # shuffle the decks
        self.card_deck_l1.shuffle()
        self.card_deck_l2.shuffle()
        self.card_deck_l3.shuffle()
        self.noble_deck.shuffle()
    
    def next_turn(self):
        """
        Method to advance to the next player's turn.
        """
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    @property
    def current_player(self):
        """
        Property to get the current player.
        """
        return self.players[self.current_player_index]




