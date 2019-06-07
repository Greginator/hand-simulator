import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class RockMullTester(MulliganTester):
    hand_types = ["theNutz","good_mix","landsAndSpells"]
    hand = Hand("decklists/gbRock.txt")
    output_file_header = "gbRock"

    def __init__(self):
        MulliganTester.__init__(self)
        self.multiSources = ["Blooming Marsh", "Overgrown Tomb", "Verdant Catacombs", "Twilight Mire", "Hissing Quagmire"]
        self.blackSource = ["Swamp"]
        self.greenSource = ["Forest", "Treetop Village"]
        self.otherLand = ["Field of Ruin"]

        self.earlyThreat = ["Dark Confidant", "Tarmogoyf", "Scavenging Ooze"]
        self.interaction = ["Thoughtseize", "Inquisition of Kozilek", "Fatal Push"]
        self.lili = ["Liliana of the Veil"]

    def CheckHand(self):
        #print("")
        #print (hand.hand_as_str())

        hand = self.hand

        numLands = hand.count_of(self.multiSources) + hand.count_of(self.blackSource) + hand.count_of(self.greenSource) + hand.count_of(self.otherLand)
        hasGreen = hand.contains(self.multiSources) or hand.contains(self.greenSource)
        hasBlack = hand.contains(self.multiSources) or hand.contains(self.blackSource)
        numEarlyThreat = hand.count_of(self.earlyThreat)
        numInteraction = hand.count_of(self.interaction)
        hasLili = hand.contains(self.lili)

        theNutz = False
        good_mix = False
        landsAndSpells = False

        if numLands >= 2 and hasGreen and hasBlack:
            if numEarlyThreat >= 1 and numInteraction >= 1:
                if hasLili:
                    theNutz = True
                elif numLands/hand.handsize() <= .5:
                    good_mix = True
                elif numLands/hand.handsize() <= .6:
                    landsAndSpells = True
            elif numLands/hand.handsize() <= .5:
                landsAndSpells = True

        results = np.array([theNutz, good_mix, landsAndSpells])
        #print(str (results))
        return results

if __name__ == "__main__":
    rockTester = RockMullTester()
    rockTester.run() 