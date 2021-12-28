############### Blackjack Project #####################


############### Our Blackjack House Rules #####################

## The deck is size n. It is a configurable number
## There are no jokers. 
## The Jack/Queen/King all count as 10.
## The the Ace can count as 11 or 1.
## Cards are removed from the deck as they are drawn.
## The dealer will draw until they have a score >= 17
## The computer is the dealer.

import art
import random

#number of decks used in a game
number_of_decks = 1 


cards = ["1","2","3","4","5","6","7","8","9","10","J","Q","K","A"]
score = [1,2,3,4,5,6,7,8,9,10,10,10,10,[1,11]]
deck = dict(zip(cards,score))



ace_scores = {}
ace_scores[0]= [0]
for aces in range(1,12):
  ace_scores[aces] = [aces+10,aces*1]


def score_calculator(hand):
  score = 0
  ace_count = hand.count("A")
  hard_deck = [card for card in hand if card != "A"]

  
  for card in hard_deck:
    score += deck[card]

  if score + max(ace_scores[ace_count]) <= 21:
    score += max(ace_scores[ace_count])
  else:
    score += min(ace_scores[ace_count])
  
  return score

def draw_card(cards):
  return random.choice(cards)


def win_checker(player_hand, dealer_hand):
  player_score = score_calculator(player_hand)
  dealer_score = score_calculator(dealer_hand)
  
  if player_score > 21:
    return "You went bust! You lose"
  elif dealer_score > 21:
    return "Win"
  elif dealer_score > player_score:
    return "Loss"
  elif player_score == dealer_score:
    return "Draw"
  else:
    return "Win"

# Define a dict to store game wins/draws/losses

log = {
  "Win" : 0,
  "Draw" : 0,
  "Loss" : 0
}

def blackjack():

  print(art.logo)
  print("Welcome to Mark's game of Blackjack.")

  complete_deck = cards * 4 * number_of_decks
  
  player_cards = []
  dealer_cards = []

  
  # Draw two cards at random for the player
  for i in range(0,2):
    player_cards.append(draw_card(complete_deck))
    complete_deck.remove(player_cards[-1])
    dealer_cards.append(draw_card(complete_deck))
    complete_deck.remove(dealer_cards[-1])

  player_choice = True

  while player_choice == True:

    #calculate player and dealer score
    player_score = score_calculator(player_cards)
    dealer_score = score_calculator(dealer_cards)
    
    print(f"Your cards are {player_cards}. Your current score is {player_score}")

    #check for blackjack (for both player and dealer) and player bust
    if player_score == 21 or dealer_score == 21 or player_score >21:
      player_choice = False

    else:
      print(f"The dealer's first card is {dealer_cards[:1]}")
    
      # Ask user to hit or stick      
      player_input = input("Type 'hit' to draw another card or 'stick' to hold tight: ")

      if player_input == "hit":
        player_cards.append(draw_card(complete_deck))
        complete_deck.remove(player_cards[-1])
      else:
        player_choice = False

  # Draw cards for dealer until score >= 17
  while score_calculator(dealer_cards) < 17:
    dealer_cards.append(draw_card(complete_deck))
    complete_deck.remove(dealer_cards[-1])
  
  
  print(f"The dealer's cards are {dealer_cards}. Score of {score_calculator(dealer_cards)}")
  print(win_checker(player_cards,dealer_cards))

  # Win/Loss/Draw tracker

  if win_checker(player_cards,dealer_cards) == "You went bust! You lose":
    log["Loss"] += 1
  else:
    log[win_checker(player_cards,dealer_cards)] += 1
  print(log)
  
  
  continue_game = input("Do you want to continue? Type 'y' or 'n': ")

  if continue_game == "y":
    blackjack()

    

blackjack()


