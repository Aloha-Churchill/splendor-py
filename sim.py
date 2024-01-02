"""

Entrypoint of the game

"""

from typing import List
from game import Game
import tkinter as tk
from computer_player import ComputerPlayer


def main():

    # create 4 computer players
    players = []
    for i in range(4):
        players.append(ComputerPlayer(f"computer{i}"))

    # initialize game
    game = Game(players)

    # simulate game until a player wins --> none of the players have 15 points
    while all(player.points < 15 for player in game.players):
        print(game)
        game.next_turn()
        game.current_player.take_turn(game)



main()