from deck import Deck
from player import Player


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
            return f"Player: {self.player.to_string()} [{self.player.hand_value()}] \r\n" \
                   f"Dealer : {self.dealer.to_string()} [{self.dealer.hand_value()}]"
        else:
            return f"Player: {self.player.to_string()} [{self.player.hand_value()}] \r\n" \
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
