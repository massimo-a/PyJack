from deck import Deck
from player import Player
from datetime import datetime


# Dealer hits on soft 17
# No splitting, no surrendering, no doubling

# Hard
# Player          Dealer
# 2 - 11          Any             H
# 12              4 - 6           S
# 13 - 16         2 - 6           S
# Else            Any             S

# Soft
# 13 - 17         Any             H
# 18              2 - 8           S
# Else            Any             S

# return 1 to stand, 0 to hit
def perfect_strategy(player: Player, dealer: Player):
    # soft totals
    if player.has_ace():
        if 13 <= player.hand_value() <= 17:
            return 0
        elif player.hand_value() == 18 and 2 <= dealer.hand[0].rank <= 8:
            return 1
        elif player.hand_value() == 18:
            return 0
        else:
            return 1
    # hard totals
    else:
        if 2 <= player.hand_value() <= 11:
            return 0
        elif player.hand_value() == 12 and 4 <= dealer.hand[0].rank <= 6:
            return 1
        elif player.hand_value() == 12:
            return 0
        elif 13 <= player.hand_value() <= 16 and 2 <= dealer.hand[0].rank <= 6:
            return 1
        elif 13 <= player.hand_value() <= 16:
            return 0
        else:
            return 1


def dealer_strategy(dealer: Player):
    if dealer.hand_value() <= 16 or (dealer.has_ace() and dealer.hand_value() <= 17):
        return 0
    else:
        return 1


class Game:
    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.count = 0
        self.dealer = Player()
        self.player = Player()

    def to_string(self, show=False):
        if show:
            return f"Player: {self.player.to_string()} \r\n" \
                   f"Dealer : {self.dealer.to_string()}"
        else:
            return f"Player: {self.player.to_string()} \r\n" \
                   f"Dealer : {self.dealer.hand[0].to_string()}"

    def count_card(self, rank):
        if 6 >= rank >= 2:
            self.count += 1
        elif rank >= 10 or rank == 1:
            self.count -= 1

    def hit_player(self):
        if self.deck.is_empty():
            self.deck = Deck()
            self.deck.shuffle()
            self.count = 0
        card = self.deck.draw()
        self.count_card(card.rank)
        self.player.hit(card)

    def hit_dealer(self):
        if self.deck.is_empty():
            self.deck = Deck()
            self.deck.shuffle()
            self.count = 0
        card = self.deck.draw()
        self.count_card(card.rank)
        self.dealer.hit(card)

    def split(self):
        pass

    def deal_cards(self):
        self.hit_player()
        self.hit_dealer()
        self.hit_player()
        self.hit_dealer()

    def play_round(self):
        self.deal_cards()
        bet = 1

        if self.count > 0:
            bet = 1 + self.count

        if self.player.hand_value() == 21:
            self.player.reset_hand()
            self.dealer.reset_hand()
            return 2 * bet

        while perfect_strategy(self.player, self.dealer) == 0:
            self.hit_player()

        if self.player.hand_value() > 21:
            self.player.reset_hand()
            self.dealer.reset_hand()
            return -bet

        while dealer_strategy(self.dealer) == 0:
            self.hit_dealer()

        win = -bet
        if self.dealer.hand_value() > 21:
            win += 2 * bet
        elif self.dealer.hand_value() > self.player.hand_value():
            pass
        elif self.dealer.hand_value() == self.player.hand_value():
            win += bet
        else:
            win += 2 * bet

        self.player.reset_hand()
        self.dealer.reset_hand()

        return win


player_profit = 0
least = 0
most = 0


def print_status():
    print("PLAYER PROFIT : " + str(player_profit))
    print("LOWEST POINT  : " + str(least))
    print("HIGHEST POINT : " + str(most))


g = Game()
start = datetime.now()

# while True:
#     now = datetime.now()
#     player_profit += g.play_round()
#     if player_profit < least:
#         least = player_profit
#     if player_profit > most:
#         most = player_profit
#
#     if (now - start).seconds > 5:
#         print_status()
#         start = datetime.now()

inp = input("Wanna play blackjack?\n\r")

game = Game()

while inp != "q":
    game.deal_cards()

    if game.player.hand_value() == 21:
        print(game.to_string(True))
        game.player.reset_hand()
        game.dealer.reset_hand()
        print("WIN! BLACKJACK!")
        break
    else:
        print(game.to_string())

    inp = input("[h]it or [s]tand?\n\r")
    while inp == "h":
        game.hit_player()
        print(game.to_string())
        if game.player.hand_value() < 21:
            inp = input("[h]it or [s]tand or [q]uit?\n\r")
        else:
            inp = "s"

    if game.player.hand_value() > 21:
        print(game.to_string(True))
        game.player.reset_hand()
        game.dealer.reset_hand()
        print("LOSS")
        break

    while dealer_strategy(game.dealer) == 0:
        game.hit_dealer()

    print(game.to_string(True))

    if game.dealer.hand_value() > 21:
        print("WIN!")
    elif game.dealer.hand_value() > game.player.hand_value():
        print("LOSS!")
    elif game.dealer.hand_value() == game.player.hand_value():
        print("WIN!")
    else:
        print("WIN!")

    game.player.reset_hand()
    game.dealer.reset_hand()

    inp = input("Another round?\n\r")
