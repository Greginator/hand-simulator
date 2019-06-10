import numpy as np
from collections import Counter
import scipy.stats as sps


class Hand:
    def __init__(self, deck_name):
        self.deck_name = deck_name
        if deck_name:
            self.deck, self.decklist = self.process(deck_name)
        else:
            self.deck = ["Storm Crow"] * 60
            self.decklist = dict(Counter(self.deck))

    def hand_as_str(self):
        return str(self.card_counts)

    def process(self, filename):
        with open(filename, "r") as file:
            file_read = [line.strip().split(" ", 1)
                         for line in file if len(line.split()) > 0]
        deck = []
        for [number, card] in file_read:
            deck += [card] * int(number)
        decklist = dict(Counter(deck))
        return deck, decklist

    def set_deck(self, new_deck):
        if isinstance(new_deck, list):
            self.deck = new_deck
            self.decklist = dict(Counter(new_deck))
        elif isinstance(new_deck, dict):
            deck = []
            for card, number in new_deck.items():
                deck += [card] * int(number)
            self.deck = deck
            self.decklist = dict(Counter(new_deck))
        elif isinstance(new_deck, str):
            self.deck, self.decklist = self.process(new_deck)
        else:
            print("ERROR: invalid deck format")
            return False
        return True

    def get_deck(self):
        return self.deck.copy()

    def get_decklist(self):
        return dict(self.decklist.copy())

    def num_subets(self):
        return self.num_subsets

    def chooseSubset(self, index):
        self.subsetIndex = index
        self.card_counts = Counter(self.subsetHands[self.subsetIndex])
        self.cards = set(self.card_counts.keys())

    def nextSubset(self):
        self.subsetIndex += 1
        self.card_counts = Counter(self.subsetHands[self.subsetIndex])
        self.cards = set(self.card_counts.keys())

    def generate_subset_hands(self, numHide):
        if numHide > 2:
            raise Exception('not implemented for more than 2')

        counterAsList = sorted(self.card_counts.elements())
        self.subsetHands = []
        for i in range(0, self.size):
            subHand = counterAsList[:i] + counterAsList[i+1:]
            if numHide > 1:
                for j in range(i, self.size-1):
                    subHand = counterAsList[:j] + counterAsList[j+1:]
                    self.subsetHands.append(subHand)
            else:
                self.subsetHands.append(subHand)

        self.num_subsets = len(self.subsetHands)
        self.subsetIndex = -1
        self.size = self.size - numHide

    def scry_bottom(self):
        self.card_counts[self.lastDraw] += -1
        self.draw_card()
        self.size += -1 #Set size after so we don't redraw this card

    def draw_card(self):
        choice = np.random.choice(len(self.deck) - self.size, 1)[0]

        if choice in self.draws:
            choice = len(self.deck) - len(self.draws) + np.where(self.draws==choice)[0][0]

        self.lastDraw = self.deck[choice]
        self.card_counts[self.lastDraw] += 1
        self.draws = np.append(self.draws, choice)
        self.cards = set(self.card_counts.keys())
        self.size += 1

    def new_hand(self, size=7):
        self.size = size
        self.draws = np.random.choice(len(self.deck), size, replace=False)
        self.card_counts = Counter([self.deck[i] for i in self.draws])
        self.cards = set(self.card_counts.keys())
        return self.card_counts.copy()

    def set_hand(self, newHand):
        self.card_counts = Counter([newHand])
        self.cards = set(self.card_counts.keys())

    def has_tron(self):
        check = [0] * 4
        if "Urza's Tower" in self.cards:
            check[0] = 1
        if "Urza's Mine" in self.cards:
            check[1] = 1
        if "Urza's Power Plant" in self.cards:
            check[2] = 1
        if "Expedition Map" in self.cards:
            check[3] = 1
        return float(sum(check) >= 3)

    def contains(self, cards):
        if isinstance(cards, str):
            return 1.0*(cards in self.cards)
        return float(len(self.cards & set(cards)) > 0)

    def count_of(self, cards):
        if isinstance(cards, str):
            return float(self.card_counts[cards])
        return float(sum([self.card_counts[card] for card in cards]))

    def handsize(self):
        return self.size

    def expect(self, cards, size=7):
        if isinstance(cards, str):
            n = self.decklist[cards]
        elif isinstance(cards, list):
            n = sum([self.decklist[card] for card in cards])
        else:
            return 0
        if n == 0:
            return 0
        return sps.hypergeom.mean(len(self.deck), n, size)
