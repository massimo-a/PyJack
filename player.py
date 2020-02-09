class Player:
    def __init__(self):
        self.hand = []

    def hit(self, c):
        self.hand.append(c)

    def to_string(self):
        str = ""
        for i in range(0, len(self.hand)-1):
            str = str + self.hand[i].to_string() + ", "
        if len(self.hand) > 0:
            return str + self.hand[len(self.hand)-1].to_string()
        else:
            return ""

    def hand_value(self):
        tot = 0
        for card in self.hand:
            if card.rank == 11 or card.rank == 12 or card.rank == 13:
                tot = tot + 10
            elif card.rank == 1:
                tot = tot + 11
            else:
                tot = tot + card.rank

        if tot > 21:
            for card in self.hand:
                if card.rank == 1 and tot > 21:
                    tot = tot - 10
        return tot

    def reset_hand(self):
        self.hand = []

    def has_ace(self):
        return list(map(lambda x: x.rank == 1, self.hand)).count(True) > 0
