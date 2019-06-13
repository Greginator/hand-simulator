import numpy as np
from hand import Hand
from mulliganTester import MulliganTester
from collections import Counter

class LimitedMullTester(MulliganTester):

    hand_types = ["PerfectCurve", "GoodCurve","keepable"]
    hand = Hand("decklists/limited.txt")
    output_file_header = "limited"
    land_value_list = ["primaryland", "secondaryland"]
    
    def __init__(self):
        MulliganTester.__init__(self)
        self.cheapPrimarySpells = ["primary12cc", "primary3cc", "primary4cc"]
        self.cheapSecondarySpells = ["secondary12cc", "secondary3cc", "secondary4cc"]
        self.primaryland = ["primaryland"]
        self.secondaryland = ["secondaryland"]
        self.twoDrop = ["primary12cc", "secondary12cc"]
        self.threeDrop = ["primary3cc", "secondary3cc"]
        self.playByThree = ["primary12cc", "secondary12cc", "primary3cc", "secondary3cc"]
        self.sortOrder = self.playByThree.copy()
        self.sortOrder.extend(["primary4cc", "secondary4cc", "fiveplus", "primaryland","secondaryland"])

    def pickBestHandSubset(self):
        handsize = self.hand.size
        self.hand.chooseSubset(None)
        card_counts = self.hand.card_counts.copy()
        newHand = []

        primaryland = self.primaryland[0]
        secondaryland = self.secondaryland[0]

        #Try to get a land of each colour - make it 3 if we have them
        if card_counts[primaryland] > 0:
            newHand.append(primaryland)
            card_counts[primaryland] += -1 
            if card_counts[secondaryland] > 0:
                newHand.append(secondaryland)
                card_counts[secondaryland] += -1 
                if card_counts[primaryland] > 0:
                    newHand.append(primaryland)
                    card_counts[primaryland] += -1 
                elif card_counts[secondaryland] > 0:
                    newHand.append(secondaryland)
                    card_counts[secondaryland] += -1 
            else:
                for i in range(0,min(2, card_counts[primaryland])):
                    newHand.append(primaryland)
        elif card_counts[secondaryland] > 0:
            for i in range(0,min(3, card_counts[secondaryland])):
                newHand.append(secondaryland)

        sortedVals = sorted(list(card_counts.elements()), key=lambda x: self.sortOrder.index(x))

        for val in sortedVals:
            newHand.append(val)
            if len(newHand) == handsize:
                break

        return self.hand.set_hand(newHand)

    def CheckHand(self):
        numPrimaryLand = self.hand.count_of(self.primaryland)
        numSecondaryland = self.hand.count_of(self.secondaryland)
        numLands = numPrimaryLand + numSecondaryland
        bothColours = numPrimaryLand > 0 and numSecondaryland > 0
        numTwoDrop = self.hand.count_of(self.twoDrop)
        numThreeDrop = self.hand.count_of(self.threeDrop)
        numEarlyPlay = numTwoDrop + numThreeDrop
        numCheapPrimary = self.hand.count_of(self.cheapPrimarySpells)
        numCheapSecondary = self.hand.count_of(self.cheapSecondarySpells)

        numSpells = self.hand.handsize() - numLands

        PerfectCurve = False
        GoodCurve = False
        keepable = False

        if numSpells >= 4 and bothColours and numTwoDrop > 0 and numEarlyPlay > 1:
            PerfectCurve = True
        elif numSpells >= 3 and bothColours and self.playByThree:
            if numLands == 2 and numTwoDrop == 0:
                keepable = True
            else:
                GoodCurve = True
        elif numSpells >= 2 and self.playByThree and ((numPrimaryLand > 0 and numCheapPrimary > 0) or (numSecondaryland > 0 and numCheapSecondary > 0)) :
            keepable = True

        results = np.array([PerfectCurve, GoodCurve, keepable])

        return results

if __name__ == "__main__":
    limitedTester = LimitedMullTester()
    limitedTester.run() 