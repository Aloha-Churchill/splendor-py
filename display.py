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

def on_gemstone_click(gemstone_type, game, root):
    messagebox.showinfo("Gemstone Clicked", f"You clicked on {gemstone_type.value}")
    current_player = game.current_player
    if current_player.can_draw_gemstone(gemstone_type, game.bank):
        current_player.draw_token(gemstone_type, 1)
        game.bank.remove_gemstones(gemstone_type, 1)
        update_display(root, game)
    else:
        messagebox.showinfo("Action Not Allowed", "Cannot draw this gemstone.")

def on_card_click(card, deck, game, root):
    current_player = game.current_player

    purchase_or_reserve = messagebox.askquestion("Purchase or Reserve", "Do you want to purchase or reserve the card? [yes to purchase/ no to reserve]", icon='warning')
    if purchase_or_reserve == 'yes':
        try:
            if current_player.can_purchase(card):
                current_player.purchase_card(card)
                deck.remove(card)
                update_display(root, game)
            else:
                messagebox.showinfo("Action Not Allowed", "Cannot purchase this card.")
        except ValueError as e:
            messagebox.showinfo("Action Not Allowed", str(e))
    elif purchase_or_reserve == 'no':
        current_player.reserve_card(card, game.bank)
        deck.remove(card)
        update_display(root, game)

def on_reserved_card_click(card, player, game, root):
    if player.can_purchase(card):
        player.purchase_card(card)
        player.reserved_cards.remove(card)
        update_display(root, game)
    else:
        messagebox.showinfo("Action Not Allowed", "Not enough resources to purchase this card.")

def create_card_frame(container, card, deck, game, root):
    frame = ttk.Frame(container, padding="10", relief=tk.RAISED)
    frame.bind("<Button-1>", lambda e, c=card, d=deck, g=game: on_card_click(c, d, g, root))
    ttk.Label(frame, text=f"Level: {card.level}").pack() if hasattr(card, 'level') else None
    cost_str = ', '.join(f"{gemstone_type.value}: {amount}" for gemstone_type, amount in card.cost.items())
    ttk.Label(frame, text=f"Cost: {cost_str}").pack()
    ttk.Label(frame, text=f"Bonus: {card.bonus.value}").pack() if hasattr(card, 'bonus') else None
    ttk.Label(frame, text=f"Points: {card.points}").pack()
    return frame

def create_bank_frame(container, bank, game, root):
    frame = ttk.Frame(container, padding="10")
    gemstone_to_column = {gemstone: index for index, gemstone in enumerate(GemstoneType)}
    for gemstone_type in GemstoneType:
        gemstone = bank.gemstones[gemstone_type]
        gemstone_frame = ttk.Frame(frame, padding="10", relief=tk.RAISED)
        gemstone_frame.grid(column=gemstone_to_column[gemstone_type], row=0, padx=5, pady=5)
        gemstone_frame.bind("<Button-1>", lambda e, gemstone_type=gemstone_type: on_gemstone_click(gemstone_type, game, root))
        ttk.Label(gemstone_frame, text=f"{gemstone.type.value}: {gemstone.quantity}").pack()
    return frame

def display_board(root, game):
    noble_frame = ttk.Frame(root, padding="10")
    noble_frame.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
    ttk.Label(noble_frame, text="Nobles:").pack(side=tk.LEFT)
    for i, noble in enumerate(game.noble_deck.items[:4]):
        create_card_frame(noble_frame, noble, game.noble_deck, game, root).pack(side=tk.LEFT)

    for level in range(3, 0, -1):
        level_frame = ttk.Frame(root, padding="10")
        level_frame.grid(row=4-level, column=0, columnspan=4, padx=5, pady=5)
        ttk.Label(level_frame, text=f"Level {level}:").pack(side=tk.LEFT)
        card_deck = getattr(game, f'card_deck_l{level}')
        for i, card in enumerate(card_deck.items[:4]):
            create_card_frame(level_frame, card, card_deck, game, root).pack(side=tk.LEFT)

    bank_frame = create_bank_frame(root, game.bank, game, root)
    bank_frame.grid(row=4, column=0, columnspan=4, padx=5, pady=5)

    display_player_info(root, game.current_player, game)

    next_turn_button = ttk.Button(root, text="Next Turn", command=lambda: update_for_next_turn(root, game))
    next_turn_button.grid(row=6, column=0, columnspan=4)

def display_player_info(root, player, game ):
    player_info_frame = ttk.Frame(root, padding=10)
    player_info_frame.grid(row=5, column=0, columnspan=4)

    # Player Name
    ttk.Label(player_info_frame, text=f"Current Player: {player.name}", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w")

    # Tokens
    tokens_str = ', '.join(f"{gemstone.value}: {quantity}" for gemstone, quantity in player.tokens.items())
    ttk.Label(player_info_frame, text="Tokens:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
    ttk.Label(player_info_frame, text=tokens_str).grid(row=2, column=0, sticky="w")

    # Points
    points_str = f"Points: {player.points}"
    ttk.Label(player_info_frame, text=points_str).grid(row=3, column=0, sticky="w")

    # Purchased Cards
    purchased_cards_str = ', '.join(f"{card.bonus.value}" for card in player.resource_cards)
    ttk.Label(player_info_frame, text="Purchased Cards:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w")
    ttk.Label(player_info_frame, text=purchased_cards_str).grid(row=5, column=0, sticky="w")

    # Reserved Cards
    ttk.Label(player_info_frame, text="Reserved Cards:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="w")
    for i, card in enumerate(player.reserved_cards):
        card_info = f"Card {i+1}: {card.bonus.value} | Points: {card.points} | Cost: {' '.join(f'{gt.value}:{amount}' for gt, amount in card.cost.items())}"
        reserved_card_button = ttk.Button(player_info_frame, text=card_info, command=lambda c=card: on_reserved_card_click(c, player, game, root))
        reserved_card_button.grid(row=7, column=i, padx=5, pady=5, sticky="w")
        
def update_display(root, game):
    for widget in root.winfo_children():
        widget.destroy()
    display_board(root, game)

def update_for_next_turn(root, game):
    game.next_turn()
    current_player = game.current_player
    acquired_noble = game.acquire_noble_if_possible(current_player)
    if acquired_noble:
        # Logic to handle drawing a new noble (if your deck supports it)
        new_noble = game.noble_deck.draw()  # Replace with your deck's method to draw a new noble
        if new_noble:
            game.noble_deck.items.append(new_noble)
        messagebox.showinfo("Noble Acquired", f"{current_player.name} has acquired a noble!")
    update_display(root, game)

