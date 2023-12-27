"""

Entrypoint of the game

"""

from deck import Deck, initialize_decks_from_csv
from bank import Bank
from display import display_board, get_player_names
from player import Player
from typing import List
from game import Game
import tkinter as tk
from computer_player import ComputerPlayer


def create_players(player_names):
    players = []
    for name in player_names:
        if "computer" in name:
            players.append(ComputerPlayer(name))
        else:
            players.append(Player(name))
    return players


def main():

    # Get player names
    player_names = get_player_names()
    # Create players
    players = create_players(player_names)
    # Create game
    game = Game(players)

    # Main window
    root = tk.Tk()
    root.title("Splendor Game")


    # Display the board with the bank
    display_board(root, game)

    # Start the GUI event loop
    root.mainloop()

main()