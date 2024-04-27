import pydealer
import matplotlib.pyplot as plt

ranks = {
    "values": {
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "Jack": 10,
        "Queen": 10,
        "King": 10,
        "Ace": 11
    }
}

#Calculate total hand value 
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        if card.value == "Ace":
            aces += 1
        value += ranks["values"][card.value]
    
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

#Create shoe for playing
def create_shoe(numDecks=6):
    shoe = pydealer.Stack()
    for int in range(numDecks):
        deck = pydealer.Deck(ranks=ranks)
        deck.shuffle()
        shoe.add(deck)
    shoe.shuffle()
    return shoe

#System for playing basic strategy
def player_action(playerHand, dealerCard, allowSplit):
    #Pair Splitting
    if allowSplit and playerHand[0].value == playerHand[1].value:
        if playerHand[0].value == 'Ace':
            return 'split'
        elif playerHand[0].value == '10':
            return 'stand'
        elif playerHand[0].value == '9':
            if dealerCard in ['7', '10', 'Ace']:
                return 'stand'
            else:
                return 'split'
        elif playerHand[0].value == '8':
            return 'split'
        elif playerHand[0].value == '7':
            if dealerCard in ['8','9', '10', 'Ace']:
                return 'hit'
            else:
                return 'stand'
        elif playerHand[0].value == '6':
            if dealerCard in ['7', '8', '9', '10', 'Ace']:
                return 'hit'
            else:
                return 'split'
        elif playerHand[0].value == '5':
            return 'stand'
        elif playerHand[0].value == '4':
            if dealerCard in ['5', '6']:
                return 'split'
            else:
                return 'hit'
        elif playerHand[0].value in ['3', '2']:
            if dealerCard in ['8', '9', '10', 'Ace']:
                return 'hit'
            else:
                return 'split'
    
    #Soft Totals
    if 'Ace' in [card.value for card in playerHand]:
        if '9' in [card.value for card in playerHand]:
            return 'stand'
        if '8' in [card.value for card in playerHand]:
            if dealerCard == '6':
                return 'double'
            else:
                return 'stand'
        if '7' in [card.value for card in playerHand]:
            if dealerCard in  ['7', '8']:
                return 'stand'
            elif dealerCard in ['9', '10', 'Ace']:
                return 'hit'
            else:
                return 'double'
        if '6' in [card.value for card in playerHand]:
            if dealerCard in ['3', '4', '5', '6']:
                return 'double'
            else:
                return 'hit'
        if '5' in [card.value for card in playerHand]:
            if dealerCard in ['4', '5', '6']:
                return 'double'
            else:
                return 'hit'
        if '4' in [card.value for card in playerHand]:
            if dealerCard in ['4', '5', '6']:
                return 'double'
            else:
                return 'hit'
        if '3' in [card.value for card in playerHand]:
            if dealerCard in ['5', '6']:
                return 'double'
            else:
                return 'hit'
        if '2' in [card.value for card in playerHand]:
            if dealerCard in ['5', '6']:
                return 'double'
            else:
                return 'hit'
    
    #Hard Totals
    playerValue = calculate_hand_value(playerHand)
    
    if playerValue >= 17:
        return 'stand'
    elif playerValue == 16:
        if dealerCard in ['2', '3', '4', '5', '6']:
            return 'stand'
        else:
            return 'hit'
    elif playerValue == 15:
        if dealerCard in ['2', '3', '4', '5', '6']:
            return 'stand'
        else:
            return 'hit'
    elif playerValue == 14:
        if dealerCard in ['2', '3', '4', '5', '6']:
            return 'stand'
        else:
            return 'hit'
    elif playerValue == 13:
        if dealerCard in ['2', '3', '4', '5', '6']:
            return 'stand'
        else:
            return 'hit'
    elif playerValue == 12:
        if dealerCard in ['4', '5', '6']:
            return 'stand'
        else:
            return 'hit'
    elif playerValue == 11:
        return 'double'
    elif playerValue == 10:
        if dealerCard in ['10', 'Ace']:
            return 'hit'
        else:
            return 'double'
    elif playerValue == 9:
        if dealerCard in ['3', '4', '5', '6']:
            return 'double'
        else:
            return 'hit'
    elif playerValue <= 8:
        return 'hit'

#Takes player decision and plays hand
def play_hand(hand, dealerHand, shoe, handName, allowSplit=True, splitCount=0, maxSplits=3):
    while True:
        action = player_action(hand, dealerHand[0], allowSplit and splitCount < maxSplits)
        print(f"{handName} decision: {action.upper()}")
        
        if action == 'split' and splitCount < maxSplits:
            return 'split'
        elif action == 'hit':
            hand.add(shoe.deal(1))
            if calculate_hand_value(hand) > 21:
                print(f"{handName}:\n", hand)
                print(f"{handName} busts! Dealer wins.")
                return "dealer"
        elif action == 'double':
            hand.add(shoe.deal(1))
            if calculate_hand_value(hand) > 21:
                print(f"{handName} after doubling down:\n", hand)
                print(f"{handName} busts! Dealer wins.")
                return "dealer"
            return "stand"
        elif action == 'stand':
            print(f"{handName} stands.")
            return "stand"

#Finishes dealer's hand
def play_dealerHand(dealerHand, playerHand, shoe):
    print("Dealer's hand:", dealerHand)

    while calculate_hand_value(dealerHand) < 17:
        dealerHand.add(shoe.deal(1))
        print("Dealer draws:", dealerHand[-1])

    dealerValue = calculate_hand_value(dealerHand)
    playerValue = calculate_hand_value(playerHand)

    print("Dealer's final hand:", dealerHand)
    if dealerValue > 21:
        print("Dealer busts. Player wins.")
        return "player"
    elif dealerValue > playerValue:
        print("Dealer stands with a higher hand. Dealer wins.")
        return "dealer"
    elif dealerValue == playerValue:
        print("It's a push. Both player and dealer have the same hand value.")
        return "push"
    else:
        print("Dealer stands with a lower hand. Player wins.")
        return "player"

#Adds results to results array
def handle_hand(playerHand, dealerHand, shoe, gameResults, splitCount=0, maxSplits=3):
    result = play_hand(playerHand, dealerHand, shoe, "Player's hand", splitCount=splitCount, maxSplits=maxSplits)
    if result == "split":
        splitCount += 1
        hand1 = pydealer.Stack(cards=[playerHand[0]])
        hand2 = pydealer.Stack(cards=[playerHand[1]])
        hand1.add(shoe.deal(1))
        hand2.add(shoe.deal(1))
        print("Playing first split hand:")
        handle_hand(hand1, dealerHand, shoe, gameResults, splitCount=splitCount, maxSplits=maxSplits)
        print("Playing second split hand:")
        handle_hand(hand2, dealerHand, shoe, gameResults, splitCount=splitCount, maxSplits=maxSplits)
    elif result == "stand":
        dealer_result = play_dealerHand(dealerHand, playerHand, shoe)
        if dealer_result == "dealer":
            gameResults.append(gameResults[-1] if gameResults else 0)
        elif dealer_result == "player":
            gameResults.append(gameResults[-1] + 1 if gameResults else 1)
        elif dealer_result == "push":
            gameResults.append(gameResults[-1] if gameResults else 0)

#Main Game loop
def play_blackjack():
    shoe = create_shoe(6)
    num_hands = int(input("How many hands? "))
    gameResults = []

    for _ in range(num_hands):
        playerHand = pydealer.Stack()
        dealerHand = pydealer.Stack()

        playerHand.add(shoe.deal(2))
        dealerHand.add(shoe.deal(2))

        print("Player's hand:\n", playerHand)
        print("Dealer's upcard:\n", dealerHand[0])

        #Check for blackjacks
        playerBlackJack = calculate_hand_value(playerHand) == 21
        dealerBlackJack = calculate_hand_value(dealerHand) == 21

        if playerBlackJack or dealerBlackJack:
            print("Dealer's hand:\n", dealerHand)
            if playerBlackJack and dealerBlackJack:
                print("Both player and dealer have blackjack. It's a push.")
                gameResults.append(gameResults[-1] if gameResults else 0)
            elif playerBlackJack:
                print("Player has a blackjack. Player wins.")
                gameResults.append(gameResults[-1] + 1 if gameResults else 1)
            elif dealerBlackJack:
                print("Dealer has a blackjack. Dealer wins.")
                gameResults.append(gameResults[-1] if gameResults else 0)
            continue

        handle_hand(playerHand, dealerHand, shoe, gameResults)

        #reshuffles shoe when low
        if len(shoe) < 20:
            shoe = create_shoe(6)
            print("Reshuffling Shoe")

        print()  #blank line after each game

    #Plot results
    plt.figure(figsize=(10, 5))
    plt.plot(gameResults, label='Wins')

    x_values = range(len(gameResults))
    y_values = [0.42 * x for x in x_values]
    plt.plot(x_values, y_values, color='r', linestyle='-', label='Average Win %')

    plt.xlabel('Number of Hands Played')
    plt.ylabel('Cumulative Wins')
    plt.title('Wins Over Time vs. Expected Win Rate')
    plt.legend()
    plt.grid(True)
    plt.show()

play_blackjack()
