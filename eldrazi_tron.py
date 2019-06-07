import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class ETronMullTester(MulliganTester):
    hand_types = ["Tron", "Chalice + 2 Lands", "t3 TKS", "t2 Reshaper", "2 Temples + Spell"]
    hand = Hand("decklists/e_tron.txt")
    output_file_header = "etron"

    def __init__(self):
        MulliganTester.__init__(self)
        self.land_names = ["Cavern of Souls", "Sea Gate Wreckage", "Wastes", "Eldrazi Temple", "Urza's Mine", "Urza's Power Plant", "Urza's Tower", "Ghost Quarter"]

    def CheckHand(self):
        hand = self.hand
        
        tron = hand.has_tron()
        lands = hand.count_of(self.land_names)
        has_TKS = hand.contains("Thought-Knot Seer")
        has_Reshaper = hand.contains("Matter Reshaper")
        has_Chalice = hand.contains("Chalice of the Void")
        temples = hand.count_of("Eldrazi Temple") 
        has_Map = float(hand.count_of("Expedition Map") > 0 and lands >= 2)
        has_Stone = hand.contains("Mind Stone")

        t3_TKS = has_TKS * (((has_Map or (temples > 0)) * (lands >= 2)) or (has_Stone * (lands >= 3)))
		# tron, Chalice + lands, t3 TKS, t2 Reshaper, 2 temples and any spell
        results = np.array([tron, has_Chalice * (lands >= 2), t3_TKS, has_Reshaper * (temples > 0) * (lands >= 2), (temples + has_Map*(lands >= 2) >= 2) * (lands < (hand.handsize()))])

        return results

if __name__ == "__main__":
    eTronTester = ETronMullTester()
    eTronTester.run() 