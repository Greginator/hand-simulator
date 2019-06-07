import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class BurnMullTester(MulliganTester):

    hand_types = ["twolandCreature","goodhand","keepable"]
    hand = Hand("decklists/burn.txt")
    output_file_header = "burn"
    
    def __init__(self):
        MulliganTester.__init__(self)
        self.rwSources = ["Bloodstained Mire", "Inspiring Vantage", "Sacred Foundry", "Scalding Tarn", "Wooded Foothills"]
        self.mountain = ["Mountain"]
        self.oneDropC = ["Goblin Guide", "Grim Lavamancer", "Monastery Swiftspear"]

    def CheckHand(self):
        #print("")
        #print (hand.hand_as_str())

        numRW = self.hand.count_of(self.rwSources)
        numLands = numRW + self.hand.count_of(self.mountain)
        numEarlyThreat = self.hand.count_of(self.oneDropC)

        twolandCreature = False
        goodhand = False
        keepable = False

        if numLands == 2 and numRW >= 1 and numEarlyThreat >= 1:
            twolandCreature = True
        elif numLands > 1 and numLands/self.hand.handsize() <= 0.6:
            goodhand = True
        elif self.hand.handsize() < 7 and numLands == 1 and numEarlyThreat == 1:
            keepable = True

        results = np.array([twolandCreature, goodhand, keepable])
        #print(str (results))
        return results

if __name__ == "__main__":
    burnTester = BurnMullTester()
    burnTester.run() 