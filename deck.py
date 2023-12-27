import random
from typing import List
import pandas as pd
from gemstone import GemstoneType
from card import Card
from card import Noble

class Deck:
    def __init__(self, items: List):
        self.items = items
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.items)

    def draw(self):
        return self.items.pop() if self.items else None

    def add(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)

    def __str__(self):
        return '\n'.join(str(item) for item in self.items)
    
    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        return iter(self.items)

def initialize_decks_from_csv(file_path: str):
    df = pd.read_csv(file_path)
    cards_l1 = []
    cards_l2 = []
    cards_l3 = []
    nobles = []

    level_mapping = {'ONE': 1, 'TWO': 2, 'THREE': 3, 'Noble': 'Noble'}

    for _, row in df.iterrows():
        level = level_mapping[row['Level']]
        if level != 'Noble':
            cost = {GemstoneType[key.upper()]: row[key] for key in ['Diamond', 'Sapphire', 'Emerald', 'Ruby', 'Onyx'] if row[key] > 0}
            bonus = GemstoneType[row['type'].upper()]
            points = row['points']
            # add card to the appropriate level
            if level == 1:
                cards_l1.append(Card(level, cost, bonus, points))
            elif level == 2:
                cards_l2.append(Card(level, cost, bonus, points))
            else:
                cards_l3.append(Card(level, cost, bonus, points))
        else:
            cost = {GemstoneType[key.upper()]: row[key] for key in ['Diamond', 'Sapphire', 'Emerald', 'Ruby', 'Onyx'] if row[key] > 0}
            points = row['points']
            nobles.append(Noble(cost, points))

    # return the decks
    return Deck(cards_l1), Deck(cards_l2), Deck(cards_l3), Deck(nobles)
