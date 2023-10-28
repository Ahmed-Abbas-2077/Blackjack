import random


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = self.get_value()

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self):
        if self.rank == "A":
            return 11
        elif self.rank in ("J", "Q", "K"):
            return 10
        else:
            return int(self.rank)


class Deck:
    def __init__(self):
        self.cards = []
        self.ranks = {"A": 11, "J": 10, "Q": 10, "K": 10, "2": 2, "3": 3,
                      "4": 4, "5": 5,  "6": 6, "7": 7, "8": 8, "9": 9, "10": 10}
        self.suits = ("Hearts", "Diamonds", "Spades", "Clubs")

        for i in self.ranks:
            for j in self.suits:
                self.cards.append(Card(i, j))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, n):
        cards_dealt = []
        for i in range(n):
            if len(self.cards) > 0:
                cards_dealt.append(self.cards.pop())
            else:
                print("No more cards to deal")
        return cards_dealt


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        sum = 0
        has_ace = False
        for card in self.cards:
            if card.rank == "A":
                has_ace = True
            sum += card.get_value()
        if has_ace and sum > 21:
            sum -= 10
        return sum

    def set_value(self):
        self.value = self.calculate_value()

    def get_value(self):
        self.set_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer \
                    and not show_all_dealer_cards and not self.is_blackjack():
                print("Hidden")
            else:
                print(card)

        if not self.dealer:
            print("Value:", self.get_value())


class Game:
    def __init__(self):
        self.player_cash = 0

    def play(self):
        self.player_cash = int(input("Enter the amount of cash you have: "))
        game_number = 0
        games_to_play = 0
        while games_to_play < 1 or games_to_play > 100:
            try:
                games_to_play = int(input(
                    "Enter the number of games you want to play 1-100: "))
            except:
                print("Please enter a positive integer from 1 to 100 !")

        while game_number < games_to_play:
            if self.player_cash < 1:
                print("You don't have enough cash to play !")
                break
            game_number += 1
            player_bet = 0
            while player_bet < 1 or player_bet > self.player_cash:
                try:
                    player_bet = int(
                        input(f"Enter your bet for game {game_number}: "))
                    if player_bet < 1:
                        print("Please enter a positive integer !")
                    elif player_bet > self.player_cash:
                        print("You don't have enough cash !")
                except:
                    print("Please enter a positive integer !")
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            if self.check_winner(player_hand, dealer_hand, game_over=False, player_bet=player_bet):
                continue

            choice = ""
            while choice not in ("S", "STAND", "H", "HIT") and player_hand.get_value() < 21:
                choice = input("Do you want to (H)it or (S)tand? ").upper()

            if choice in ("H", "HIT"):
                player_hand.add_card(deck.deal(1))
                player_hand.display()

            if self.check_winner(player_hand, dealer_hand, player_bet=player_bet):
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand.get_value() < 17:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_cards=True)

            if self.check_winner(player_hand, dealer_hand, player_bet=player_bet, game_over=True):
                continue

            print("Final hands:")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)
            print("Your cash:", self.player_cash)

            self.check_winner(player_hand, dealer_hand,
                              player_bet=player_bet, game_over=True)

        print("\nThanks for playing !")

    def check_winner(self, player_hand, dealer_hand, player_bet, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You busted, you lose!")
                self.player_cash -= player_bet
                print("Your cash:", self.player_cash)
                return True
            elif dealer_hand.get_value() > 21:
                print("Dealer busted, you win!")
                self.player_cash += player_bet
                print("Your cash:", self.player_cash)
                return True
            elif player_hand.is_blackjack() and dealer_hand.is_blackjack():
                print("Both players have blackjack, it's a tie!")
                print("Your cash:", self.player_cash)
                return True
            elif player_hand.is_blackjack():
                print("You have blackjack, you win!")
                self.player_cash += player_bet * 1.5
                print("Your cash:", self.player_cash)
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer has blackjack, you lose!")
                self.player_cash -= player_bet
                print("Your cash:", self.player_cash)
                return True
        else:
            if player_hand.get_value() == dealer_hand.get_value():
                print("Both players have the same score, it's a tie!")
                print("Your cash:", self.player_cash)
                return True
            elif player_hand.get_value() > dealer_hand.get_value() and player_hand.get_value() <= 21:
                print("You beat the dealer, you win!")
                self.player_cash += player_bet
                print("Your cash:", self.player_cash)
                return True
            elif dealer_hand.get_value() > player_hand.get_value() and dealer_hand.get_value() <= 21:
                print("Dealer beat you, you lose!")
                self.player_cash -= player_bet
                print("Your cash:", self.player_cash)
                return True
        return False


g = Game()
g.play()
