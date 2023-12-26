import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from gemstone import GemstoneType
from tkinter import simpledialog

def get_player_names():
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    player_names = []
    while True:
        name = simpledialog.askstring("Player Name", "Enter player name (or leave blank to finish):", parent=root)
        if not name:
            break
        player_names.append(name)
    root.destroy()
    return player_names


def on_card_click(card, deck, game):
    """
    Callback function for when a card is clicked.
    """
    messagebox.showinfo("Card Selected", f"You selected: {card}")
    # Add logic for card selection here, using the game object
    # Check if the current player can purchase the card
    if game.current_player.can_purchase(card):
        game.current_player.purchase_card(card)
        deck.remove(card)
        update_display(root, game)  # Update the display to reflect the changes
    else:
        messagebox.showinfo("Action Not Allowed", "You do not have enough resources to purchase this card.")


def on_gemstone_click(gemstone_type, game):
    """
    Callback function for when a gemstone in the bank is clicked.
    """
    messagebox.showinfo("Gemstone Selected", f"You selected: {gemstone_type}")
    # Add logic for gemstone selection here, using the game object
    if game.bank.can_remove_gemstone(gemstone_type, 1):
        game.bank.remove_gemstones(gemstone_type, 1)
        game.current_player.add_token(gemstone_type, 1)
        update_display(root, game)  # Update the display to reflect the changes


def create_card_frame(container, card, deck, game):
    frame = ttk.Frame(container, padding=10, relief=tk.RAISED)
    frame.bind("<Button-1>", lambda e: on_card_click(card, deck, game))
    ttk.Label(frame, text=f"Level: {card.level}").pack() if hasattr(card, 'level') else None
    cost_str = ', '.join(f"{gemstone_type.value}: {amount}" for gemstone_type, amount in card.cost.items())
    ttk.Label(frame, text=f"Cost: {cost_str}").pack()
    ttk.Label(frame, text=f"Bonus: {card.bonus.value}").pack() if hasattr(card, 'bonus') else None
    ttk.Label(frame, text=f"Points: {card.points}").pack()
    return frame

def create_bank_frame(container, bank, game):
    frame = ttk.Frame(container, padding=10)
    for gemstone_type in GemstoneType:
        gemstone = bank.gemstones[gemstone_type]
        gemstone_frame = ttk.Frame(frame, padding=5, relief=tk.RAISED)
        gemstone_frame.pack(side=tk.LEFT)
        gemstone_frame.bind("<Button-1>", lambda e, gemstone=gemstone_type: on_gemstone_click(gemstone, game))
        ttk.Label(gemstone_frame, text=f"{gemstone.type.value}: {gemstone.quantity}").pack()
    return frame

def display_board(root, game):
    # Displaying the noble deck
    noble_frame = ttk.Frame(root, padding=10)
    noble_frame.grid(row=0, column=0, columnspan=4)
    ttk.Label(noble_frame, text="Nobles:").pack(side=tk.LEFT)
    for i, noble in enumerate(game.noble_deck.items[:4]):
        create_card_frame(noble_frame, noble, game.noble_deck, game).pack(side=tk.LEFT)

    # Displaying each level of card decks
    for level in range(3, 0, -1):
        level_frame = ttk.Frame(root, padding=10)
        level_frame.grid(row=4-level, column=0, columnspan=4)
        ttk.Label(level_frame, text=f"Level {level}:").pack(side=tk.LEFT)
        card_deck = getattr(game, f'card_deck_l{level}')
        for i, card in enumerate(card_deck.items[:4]):
            create_card_frame(level_frame, card, card_deck, game).pack(side=tk.LEFT)

    # Displaying the bank
    bank_frame = create_bank_frame(root, game.bank, game)
    bank_frame.grid(row=4, column=0, columnspan=4)

    # Display current player info
    display_player_info(root, game.current_player)

    # You might want to add a button or mechanism to go to the next turn
    next_turn_button = ttk.Button(root, text="Next Turn", command=lambda: update_for_next_turn(root, game))
    next_turn_button.grid(row=6, column=0, columnspan=4)

def update_for_next_turn(root, game):
    game.next_turn()
    # Clear and update the GUI with new player info
    for widget in root.winfo_children():
        widget.destroy()
    display_board(root, game)


def display_player_info(root, player):
    player_info_frame = ttk.Frame(root, padding=10)
    player_info_frame.grid(row=5, column=0, columnspan=4)
    ttk.Label(player_info_frame, text=f"Current Player: {player.name}").pack(side=tk.LEFT)
    tokens_str = ', '.join(f"{gemstone.value}: {quantity}" for gemstone, quantity in player.tokens.items())
    ttk.Label(player_info_frame, text=f"Tokens: {tokens_str}").pack(side=tk.LEFT)
    points_str = f"Points: {player.points}"
    ttk.Label(player_info_frame, text=points_str).pack(side=tk.LEFT)
    # You can add more details like resource cards, reserved cards, etc.

def update_display(root, game):
    # Clear the current GUI elements
    for widget in root.winfo_children():
        widget.destroy()
    # Redraw the board with updated game state
    display_board(root, game)