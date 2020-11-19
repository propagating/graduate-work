# Ryan Richardson
# CS 532
# HW 1 - Flush Simulation

import random

deck = []
suits = ['D', 'H', 'C', 'S']
cards = range(1, 14)


def buildDeck():
    for c in cards:
        for j in suits:
            deck.append((c, j))


def checkFlush(hand):
    handSuits = set(list(zip(*hand))[1])  # get all unique suits
    if len(handSuits) == 1:  # check only 1 suit exists
        handCards = set(list(zip(*hand))[0])  # get set of cards in hand
        rankMax = max(handCards)
        rankMin = min(handCards)
        rank = rankMax - rankMin + 1
        if cards == [1, 10, 11, 12, 13]:  # handle the Ace Rollover in a Royal Flush as a special case
            return 0
        elif rank == len(
                hand):  # only way for the rank to be equal to the length of the hand is if each card is separated by exactly 1 from its nearest neighbour
            return 0
        else:
            return 1
    return 0


def checkFullHouse(hand):
    cardValues = list(zip(*hand))[0]  # get values of each card in hand without their suit
    handCards = set(cardValues)  # get unique values of cards in hand
    faceCards = set([11, 12, 13])  # create set of face cards we're interested in

    if len(handCards) == 2:  # check only 2 unique card values exist in hand
        if set(faceCards & set(handCards)):  # check we have at least 1 face card
            inter = handCards.intersection(faceCards)  # get value(s) of face card(s) the hand
            for i in inter:  # for each face card that exists in hand
                countInHand = cardValues.count(i)  # get count of face card in hand
                if countInHand == 2:  # if count is exactly 2, we have a pair of face cards and return a positive value
                    return 1
            return 0
        return 0
    return 0


def deal(deck, n):  # deck, n = no. of cards
    return random.sample(deck, n)


buildDeck()
iters = 0
x = 0

import itertools

for hand in itertools.combinations(deck, 5):
    x += checkFullHouse(hand)
    iters += 1
    if iters % 100000 == 0:
        print(f"Total flush hands {x}\nTotal Iterations {iters}\nFlush Pair Probability {x/iters}")

print(f"Total flush hands {x}\nTotal Iterations {iters}\nFlush Pair Probability {x / iters}")