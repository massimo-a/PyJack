import random

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def to_string(self):
        r = self.rank
        if self.rank == 11:
            r = "Jack"
        elif self.rank == 12:
            r = "Queen"
        elif self.rank == 13:
            r = "King"
        elif self.rank == 1:
            r = "Ace"
        return f"{r} of {self.suit}"

class Deck:
    def __init__(self, numDecks = 1):
        self.cards = []
        for card in range(1, 14):
            for i in range(0, numDecks):
                self.cards.append(Card(card, "Diamonds"))
                self.cards.append(Card(card, "Hearts"))
                self.cards.append(Card(card, "Spades"))
                self.cards.append(Card(card, "Clubs"))

    def draw(self):
        return self.cards.pop(0)

    def shuffle(self):
        random.shuffle(self.cards)
