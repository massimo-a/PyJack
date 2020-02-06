from deck import Deck
from player import Player

class Strategy:
    pass

class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Player()
        self.player = Player()

    def to_string(self):
        return f"Player: {self.player.to_string()} \r\n" \
            f"Dealer : {self.dealer.to_string()}"

    def hitPlayer(self):
        card = self.deck.draw()
        self.player.hit(card)

    def hitDealer(self):
        card = self.deck.draw()
        self.dealer.hit(card)

    def dealCards(self):
        self.hitPlayer()
        self.hitDealer()
        self.hitPlayer()
        self.hitDealer()

    def playRound(self):
        self.dealCards()

        if self.player.handValue() == 21:
            self.player.resetHand()
            self.dealer.resetHand()
            return 3

        while self.player.handValue() < 17:
            self.hitPlayer()

        if self.player.handValue() > 21:
            self.player.resetHand()
            self.dealer.resetHand()
            return 0

        while self.dealer.handValue() < 17:
            self.hitDealer()

        win = 0
        if self.dealer.handValue() > 21:
            win = 2
        elif self.dealer.handValue() > self.player.handValue():
            pass
        elif self.dealer.handValue() == self.player.handValue():
            win = 1
        else:
            win = 2

        self.player.resetHand()
        self.dealer.resetHand()

        return win

playerWins = 0
totalGames = 0

for j in range(0, 1000):
    g = Game()
    for i in range(0, 5):
        playerWins = playerWins + g.playRound()
        totalGames = totalGames + 1

print(playerWins - totalGames)