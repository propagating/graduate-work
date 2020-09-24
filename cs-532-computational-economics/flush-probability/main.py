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


def deal(deck, n):  # deck, n = no. of cards
    return random.sample(deck, n)


buildDeck()

x = 0
for i in range(200000):
    x += checkFlush(deal(deck, 5))

print(x / 200000)
