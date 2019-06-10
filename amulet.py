import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class AmuletMullTester(MulliganTester):

    hand_types = ["#TheNutz", "stirNutz", "double amulet", "t3/4 titan", "solid keep"]
    hand = Hand("decklists/amulet.txt")
    output_file_header = "amulet"

    def __init__(self):
        MulliganTester.__init__(self)
        self.one_mana_lands = ["Forest", "Bojuka Bog", "Botanical Sanctum", "Cavern of Souls", "Gemstone Mine", "Kabira Crossroads", "Khalni Garden", "Slayers' Stronghold", "Sunhome, Fortress of the Legion", "Tolaria West"]
        self.vesuva = ["Vesuva"]
        self.bounce_lands = ["Boros Garrison", "Selesnya Sanctuary", "Simic Growth Chamber"]
        self.green_source = ["Forest", "Botanical Sanctum", "Cavern of Souls", "Selesnya Sanctuary", "Simic Growth Chamber", "Gemstone Mine", "Khalni Garden"] 
        self.amulet = ["Amulet of Vigor"]
        self.ramp_dudes = ["Azusa, Lost but Seeking", "Sakura-Tribe Scout", "Coalition Relic"]
        self.payoff = ["Hive Mind", "Primeval Titan", "Summoner's Pact", "Tolaria West"]
        self.the_fat = ["Hive Mind", "Primeval Titan", "Walking Ballista", "Pact of Negation", "Summoner's Pact"]
        self.stir = ["Ancient Stirrings"]
        self.relic = ["Coalition Relic"]

    def CheckHand(self):
        #print("")
        #print (hand.hand_as_str())
        
        hand = self.hand

        num_reg_land = hand.count_of(self.one_mana_lands)
        num_vesuva = hand.count_of(self.vesuva)
        num_bounce = hand.count_of(self.bounce_lands)
        land_mana = num_reg_land + 2*num_bounce + (num_vesuva if num_bounce == 0 else num_vesuva*2)
        num_green_source = hand.count_of(self.green_source)
        
        num_amulet = hand.count_of(self.amulet)
        num_payoff = hand.count_of(self.payoff)
        num_stir = hand.count_of(self.stir)
        num_relic = hand.count_of(self.relic)
        num_ramp_dudes = hand.count_of(self.ramp_dudes)
        num_high_cc = hand.count_of(self.the_fat)

        num_mana = land_mana + (num_amulet if num_bounce > 1 else 0) + num_relic*2 + (1 if num_stir and num_green_source else 0)
        has_6_mana = land_mana >= 3 and num_mana >= 6
        nutz_count = 0
        nutz_count += num_amulet > 0
        nutz_count += num_ramp_dudes > 0
        nutz_count += num_reg_land > 0
        nutz_count += num_green_source > 0
        nutz_count += num_payoff > 0
        nutz_count += has_6_mana

        is_nutz = False
        stir_nutz = False
        double_amulet = False
        is_t4_titan = False
        solid_keep = False

        if nutz_count >= 6:
            is_nutz = True
        elif num_reg_land > 0 and num_green_source > 0 and nutz_count + num_stir >= 6:
            stir_nutz = True
        elif num_amulet > 1 and land_mana > 1 and (num_bounce > 0 or (num_green_source > 0 and num_reg_land > 0 and num_stir > 0)):
            double_amulet = True
        elif num_ramp_dudes > 0 and num_payoff > 0 and has_6_mana:
            is_t4_titan = True
        elif num_reg_land > 0 and num_green_source > 0 and nutz_count + num_stir >= 5 and hand.handsize() - num_high_cc > 4:
            solid_keep = True

        results = np.array([is_nutz, stir_nutz, double_amulet, is_t4_titan, solid_keep])
        #print(str (results))

        return results

if __name__ == "__main__":
    amuletTester = AmuletMullTester()
    amuletTester.run() 