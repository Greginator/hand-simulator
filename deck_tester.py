import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class TestDeckMullTester(MulliganTester):

    #has to equal hand names lower down
    hand_types = ["ShouldNotBeOk", "ShouldBeOK"]
    hand = Hand("decklists/test_deck.txt")
    output_file_header = "Tester"
    land_value_list = ["Mana Confluence", "Cephalid Coliseum"]


    def __init__(self):
        MulliganTester.__init__(self)

    def CheckHand(self):

        hand = self.hand

        #print("")
        #print (hand.hand_as_str())
        #numTron = hand.contains(self.tron1) + hand.contains(self.tron2) + hand.contains(self.tron3)

        #criteria

#         numStir = hand.count_of(self.stir) if hasGreen else 0
#         numPayoff = hand.count_of(self.payoff)
#         hasKarn = hand.contains(self.karn)
#         tronFinders = hand.count_of(self.exmap) + hand.count_of(self.sylv) if hasGreen else 0
#         numLand = hand.count_of(self.land_value_list)
#         numCantrips = hand.count_of(self.cantrips) + numStir
#         hasOStone = hand.contains(self.ostone)

        ShouldNotBeOk = False
        ShouldBeOk = False

        if ( hand.count_of("Mana Confluence") > 5):
            ShouldNotBeOk = True


        if ( hand.count_of("Mana Confluence") > 4 ):
            ShouldBeOk = True
        
        
        results = np.array([ShouldNotBeOk, ShouldBeOk])
        #results = np.array([t3karnGG, tronWPayoff, justTron, keepable])
        #print(str (results))
        return results

if __name__ == "__main__":
    testDeckMullTester = TestDeckMullTester()
    testDeckMullTester.run() 