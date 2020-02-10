from game import Game, dealer_strategy
from datetime import datetime
from colorama import init
from colorama import Fore, Style

init()
player_profit = 0
least = 0
most = 0

print("\033[H\033[J")


def print_status():
    print("\033[H\033[J")
    print("PLAYER PROFIT : " + str(player_profit))
    print("LOWEST POINT  : " + str(least))
    print("HIGHEST POINT : " + str(most))


def game_status(game, b):
    print("\033[H\033[J")
    print(game.to_string(b))


game = Game()

inp = input("Run [s]imulation or [p]lay?\n\r")

if inp == "s":
    start = datetime.now()

    while True:
        now = datetime.now()
        player_profit += game.play_round()
        if player_profit < least:
            least = player_profit
        if player_profit > most:
            most = player_profit

        if (now - start).seconds > 5:
            print_status()
            start = datetime.now()
elif inp == "p":
    while inp != "q":
        game.deal_cards()

        if game.dealer.hand_value() == 21 and game.player.hand_value() == 21:
            game_status(game, True)
            game.player.reset_hand()
            game.dealer.reset_hand()
            print(Fore.YELLOW + 'PUSH!')
            print(Style.RESET_ALL)
        elif game.dealer.hand_value() == 21:
            game_status(game, True)
            game.player.reset_hand()
            game.dealer.reset_hand()
            print(Fore.RED + 'LOSS!')
            print(Style.RESET_ALL)
        elif game.player.hand_value() == 21:
            game_status(game, True)
            game.player.reset_hand()
            game.dealer.reset_hand()
            print(Fore.GREEN + 'WIN! BLACKJACK!')
            print(Style.RESET_ALL)
        else:
            game_status(game, False)

            inp = input("[h]it or [s]tand?\n\r")
            while inp == "h":
                game.hit_player()
                game_status(game, False)
                if game.player.hand_value() < 21:
                    inp = input("[h]it or [s]tand?\n\r")
                else:
                    inp = "s"

            if game.player.hand_value() > 21:
                game_status(game, True)
                game.player.reset_hand()
                game.dealer.reset_hand()
                print(Fore.RED + 'LOSS!')
                print(Style.RESET_ALL)
            else:
                while dealer_strategy(game.dealer) == 0:
                    game.hit_dealer()

                game_status(game, True)

                if game.dealer.hand_value() > 21:
                    print(Fore.GREEN + 'WIN!')
                    print(Style.RESET_ALL)
                elif game.dealer.hand_value() > game.player.hand_value():
                    print(Fore.RED + 'LOSS!')
                    print(Style.RESET_ALL)
                elif game.dealer.hand_value() == game.player.hand_value():
                    print(Fore.YELLOW + 'PUSH!')
                    print(Style.RESET_ALL)
                else:
                    print(Fore.GREEN + 'WIN!')
                    print(Style.RESET_ALL)

        game.player.reset_hand()
        game.dealer.reset_hand()

        inp = input("Another round? (q to quit)\n\r")
