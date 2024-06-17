from colorama import Fore, Style
import math
import random
import time

card_values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
suits = ["♥", "♦", "♣", "♠"]

used_cards = []

balance = 5000

reset = Style.RESET_ALL
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
blue = Fore.BLUE

logo = f"""{red}
██████╗░██╗░░░░░░█████╗░░█████╗░██╗░░██╗░░░░██╗░█████╗░░█████╗░██╗░░██╗
██╔══██╗██║░░░░░██╔══██╗██╔══██╗██║░██╔╝░░░░██║██╔══██╗██╔══██╗██║░██╔╝
██████╔╝██║░░░░░███████║██║░░╚═╝█████╔╝░░░░░██║███████║██║░░╚═╝█████╔╝░
██╔══██╗██║░░░░░██╔══██║██║░░██╗██╔═██╗░██░░██║██╔══██║██║░░██╗██╔═██╗░
██████╔╝███████╗██║░░██║╚█████╔╝██║░░██╗╚█████║██║░░██║╚█████╔╝██║░░██╗
╚═════╝░╚══════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝░╚════╝╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝
{reset}"""
    
def clear():
  print("\033c", end = "", flush = True)

def rules():
  print(f"""
1. Objective: Beat the Dealer's hand without going over 21

2. Card Values:
  • Numbered cards (2-10) are worth their face value
  • Face cards (J, Q, K) are each worth 10 points
  • Aces can be worth 1 or 11 points, depending on what help your hand
  
3. Dealing:
  • The dealer deals two cards to the player and to themselves
  • One of the dealer's cards are dealt upright (\"upcard\"), while the other is faced down (\"hole card\")

4. Player Turn:
  • Player decides whether to \"{red}hit{reset}\" (receive another card) or to \"{green}stand{reset}\" (keep their current hand)

5. Dealer Turn:
  • After player stands, dealer will reveal their hole card
  • Dealer must hit if their total is 16 or less and stand on 17 or higher

6. Winning and Losing:
  • If a player's total exceeds 21, they bust and lose the round.
  • If the dealer {red}busts{reset}, the player wins.
  • If neither the player nor the dealer busts, the hand with the total closest to 21 wins.
  • If the player's total is the same as the dealer's, it's a push (tie), and the player's bet is returned.
  • If the player {green}wins{reset}, the player earns the amount they wagered

7. Blackjack:
  • If the player is dealt an ace and a 10-point card as their initial cards, they have a {yellow}blackjack{reset}
  • A {yellow}blackjack{reset} pays 1.5 times the wager (If you wager {green}$10{reset}, then you earn {green}$15{reset})
""")

def start():
  while True:
    print(f"What is your choice?\n\n{green}1. Rules\n\n{yellow}2. Start blackjack game\n{reset}")

    try:
      choice = int(input("Enter your choice: "))
      if choice in [1, 2]:
        break
    except ValueError:  
      pass

    print("Invalid input")
    time.sleep(2)
    clear()
    
  clear()

  return choice
  
def make_cards(suit = "h", value = "h"):
  card = [
    "┌─────────┐",
    "│{:<2}       │".format(value),
    "│         │",
    "│         │",
    "│    {}    │".format(suit),
    "│         │",
    "│         │",
    "│       {:>2}│".format(value),
    "└─────────┘"
  ]

  hidden_card = [
    "┌─────────┐",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "│░░░░░░░░░│",
    "└─────────┘"
  ]
  
  if suit == "h" and value == "h":
    return hidden_card
  else:
    return card

def convert_card_values(card):
  if card in ["J", "Q", "K"]:
    return 10
  elif card == "A":
    return 11
  else:
    return int(card)
    
def adjust_ace_value(hand):
  ace_positions = []

  for index, value in enumerate(hand):
    if value == 11:
      ace_positions.append(index)

  for index in ace_positions:
    if sum(hand) > 21:
      hand[index] = 1

  return hand

def get_new_card():
  while True:
    new_card = [random.choice(suits), random.choice(card_values)]

    if new_card not in used_cards:
      used_cards.append(new_card)
      return new_card
  
def deal_cards():
  while True:
    hand = []

    while len(hand) < 2:
      hand.append(get_new_card())
    
    numeric_hand = [convert_card_values(card[1]) for card in hand]

    return hand, numeric_hand

def get_wager(balance):
  while True:
    print(f"Welcome! Your balance is {green}${balance}{reset}")

    try:
      wager = int(input("How much do you want to wager? "))

      if wager < 100:
        print(f"You gotta bet at least {green}$100{reset}")
      elif wager > balance:
        print("You can't bet more than you have.")
      else:
        return wager
    except ValueError:
      print("Please enter a positive integer")

    time.sleep(2)
    clear()

def display_cards(cards):
  for i in range(9):
    print(" ".join(card[i] for card in cards))

def display_info(wager, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards, decision = "hit"):
  if decision == "hit":
    dealer_total = dealer_numeric_hand[0]
  else:
    dealer_total = sum(dealer_numeric_hand)
      
  print(f"Wager: {green}{wager}{reset} | Balance: {green}{balance}{reset}\n")

  print(f"Player's Cards │ Total: {blue}{sum(player_numeric_hand)}{reset}")
  display_cards(player_cards)

  print(f"\nDealer's Cards | Total: {blue}{dealer_total}{reset}")
  display_cards(dealer_cards)

def payout(wager, balance, player_numeric_hand, dealer_numeric_hand, state, dealer_state):
  if state == "bust":
    print(f"\n{red}Bust!{reset} You Lost.")
    balance -= wager
  elif state == "blackjack":
    if dealer_state == "blackjack":
      print("\nBummer. You tied.")
    else:
      print(f"\n{yellow}Blackjack!{reset} You Win!")
      balance += math.floor(wager * 1.5)
  elif state == "stand":
    if dealer_state == "blackjack":
      print("\nYou lost. Better luck next time.")
      balance -= wager
    elif dealer_state == "bust" or sum(player_numeric_hand) > sum(dealer_numeric_hand):
      print("\nCongrats! You Win!")
      balance += wager
    elif sum(player_numeric_hand) < sum(dealer_numeric_hand):
      print("\nYou lost. Better luck next time.")
      balance -= wager
    else:
      print("\nBummer. You tied.")
  else:
    print("\nYou lost. Better luck next time.")
    balance -= wager

  return balance

def user_decision(wager, hand, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards):
  while True:
    display_info(wager, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards)
    
    choice = input(f"\nWhould you like to {red}hit (h){reset} or {green}stand (s){reset}\n").lower().strip()

    if choice.isalpha():
      if choice == "h":
        new_card = get_new_card()
        hand.append(new_card)
        numeric_new_card = convert_card_values(new_card[1])
        player_numeric_hand.append(numeric_new_card)
        player_cards.append(make_cards(new_card[0], new_card[1]))
        player_numeric_hand = adjust_ace_value(player_numeric_hand)
        clear()
        display_info(wager, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards)
        if sum(player_numeric_hand) > 21:
          return "bust", player_numeric_hand
        clear()
        continue
      elif choice == "s":
        clear()
        return "stand", player_numeric_hand
      
    print("Please type in a valid option")
    time.sleep(2)
    clear()

def dealer_turn(wager, hand, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards, dealer_state = "none"):
  while True:
    display_info(wager, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards, decision = "stand")

    if sum(dealer_numeric_hand) < 17:
      new_card= get_new_card()
      hand.append(new_card)
      numeric_new_card = convert_card_values(new_card[1])
      dealer_numeric_hand.append(numeric_new_card)
      dealer_cards.append(make_cards(new_card[0], new_card[1]))
      dealer_numeric_hand = adjust_ace_value(dealer_numeric_hand)
      clear()
      display_info(wager, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards, decision = "stand")
    elif sum(dealer_numeric_hand) > 21:
      return "bust", dealer_numeric_hand
    else:
      if dealer_state == "blackjack":
        return dealer_state, dealer_numeric_hand
      return "stand", dealer_numeric_hand
    time.sleep(0.5)
    clear()
    
def play_hand(player_hand, player_numeric_hand, dealer_hand, dealer_numeric_hand, wager, balance):
  player_cards = [make_cards(card[0], card[1]) for card in player_hand]
  dealer_cards = [make_cards(dealer_hand[0][0], dealer_hand[0][1]), make_cards()]
  dealer_state = "none"

  if sum(player_numeric_hand) == 21:
    state = "blackjack"
  else:
    state, player_numeric_hand = user_decision(wager, player_hand, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards)

  if state != "bust":
    if sum(dealer_numeric_hand) != 21:
      dealer_cards = [make_cards(card[0], card[1]) for card in dealer_hand]
      dealer_state, dealer_numeric_hand = dealer_turn(wager, dealer_hand, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards)
    else:
      dealer_cards = [make_cards(card[0], card[1]) for card in dealer_hand]
      dealer_state, dealer_numeric_hand = dealer_turn(wager, dealer_hand, balance, player_numeric_hand, dealer_numeric_hand, player_cards, dealer_cards, dealer_state)
      dealer_state = "blackjack"
  else:
    dealer_state = "stand"

  return payout(wager, balance, player_numeric_hand, dealer_numeric_hand, state, dealer_state)

def play_again():
  while True:
    replay = input(f"Would you like to play again? ({green}y{reset}/{red}n{reset}) ")
    if replay.isalpha() and replay in ["y", "n"]:
      return replay
    print("Enter a valid option")
    time.sleep(2)
    print("\x1b[3A\x1b[0J")
  
def blackjack(balance):
  while True:
    player_hand, player_numeric_hand = deal_cards()
    dealer_hand, dealer_numeric_hand = deal_cards()
    wager = get_wager(balance)
    clear()

    balance = play_hand(player_hand, player_numeric_hand, dealer_hand, dealer_numeric_hand, wager, balance)
    print(f"Your balance is {green}{balance}{reset}\n")

    if balance < 100:
      print("You don't have enough money")
      break
    
    replay = play_again()
    if replay.lower() == "n":
      break

    clear()
    used_cards.clear()

  if balance >= 100:
    print(f"\nThanks for playing! Your final balance was {green}{balance}{reset}")
  else:
    print("\nThanks for playing!")

print(logo)
input(f"Press [{blue}ENTER{reset}] to start\n")
clear()

while True:
  choice = start()

  if choice == 1:
    rules()
    input(f"Press [{blue}ENTER{reset}] when you are finished reading\n")
    clear()
  else:
    break
    
blackjack(balance)
time.sleep(5)
clear()