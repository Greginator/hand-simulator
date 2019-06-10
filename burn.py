import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class BurnMullTester(MulliganTester):

    hand_types = ["twolandCreature","goodhand","keepable"]
    hand = Hand("decklists/burn.txt")
    output_file_header = "burn"
    land_value_list = ["Mountain", "Bloodstained Mire", "Inspiring Vantage", "Sacred Foundry", "Scalding Tarn", "Wooded Foothills"]
    
    def __init__(self):
        MulliganTester.__init__(self)
        self.rwSources = ["Bloodstained Mire", "Inspiring Vantage", "Sacred Foundry", "Scalding Tarn", "Wooded Foothills"]
        self.mountain = ["Mountain"]
        self.oneDropC = ["Goblin Guide", "Grim Lavamancer", "Monastery Swiftspear"]

    def CheckHand(self):
        numRW = self.hand.count_of(self.rwSources)
        numLands = numRW + self.hand.count_of(self.mountain)
        numEarlyThreat = self.hand.count_of(self.oneDropC)

        twolandCreature = False
        goodhand = False
        keepable = False

        numSpells = self.hand.handsize() - numLands

        if numSpells >= 5 and numRW >= 1 and numEarlyThreat >= 1:
            twolandCreature = True
        elif numLands > 1 and (numSpells >= 4 or (numSpells >= 3 and numEarlyThreat > 0)):
            goodhand = True
        elif numLands > 1 and numSpells >= 3:
            keepable = True
        elif numLands == 1 and numEarlyThreat > 1:
            keepable = True

        results = np.array([twolandCreature, goodhand, keepable])

        return results

if __name__ == "__main__":
    burnTester = BurnMullTester()
    burnTester.run() 