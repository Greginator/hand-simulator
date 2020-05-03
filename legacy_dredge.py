import numpy as np
from hand import Hand
from mulliganTester import MulliganTester

class DredgeMullTester(MulliganTester):

    #has to equal hand names lower down
    hand_types = ["theNuts", "strongLedAndLoot", "weakLedAndLoot", "strongThreeLootAndDredge", "weakThreeLootAndDredge", "threeLootNoDredge", "twoLootAndDredge"]
    hand = Hand("decklists/led_dredge.txt")
    output_file_header = "LED Dredge"
    land_value_list = ["Mana Confluence", "Gemstone Mine", "City of Brass", "Cephalid Coliseum"]

    def __init__(self):
        MulliganTester.__init__(self)

        self.gold_source = ["Mana Confluence", "Gemstone Mine", "City of Brass"]
        self.loot = ["Faithless Looting", "Careful Study"]
        self.faithless = ["Faithless Looting", "Careful Study"]
        self.dredger = ["Golgari Grave-Troll", "Stinkweed Imp", "Golgari Thug"]
        self.good_dredger = ["Golgari Grave-Troll", "Stinkweed Imp"]
        self.breakthrough = ["Breakthrough"]
        self.study = ["Careful Study"]
        self.pimp = ["Putrid Imp"]
        self.led = ["Lion's Eye Diamond"]
        self.coliseum = ["Cephalid Coliseum"]
        self.petal = ["Lotus Petal"]

    def CheckHand(self):

        hand = self.hand

        #print("")
        #print (hand.hand_as_str())
        #numTron = hand.contains(self.tron1) + hand.contains(self.tron2) + hand.contains(self.tron3)

        #criteria
        hasGold = hand.contains(self.gold_source)
        goldCount = hand.count_of(self.gold_source)
        hasColiseum = hand.contains(self.coliseum)
        hasBlue = hand.contains(self.gold_source) or hand.contains(self.coliseum)
        hasDredge = hand.contains(self.dredger)
        hasGoodDredgerOrMoreThanOne = hand.count_of(self.dredger) > 1 or hand.contains(self.good_dredger)
        hasPimp = hand.contains(self.pimp)
        combinedNumPimpLoot = hand.contains(self.pimp) + hand.count_of(self.loot)
        hasLed = hand.contains(self.led)
        hasLooting = hand.contains(self.faithless)
        hasBlueLoot = hand.contains(self.breakthrough) or hand.contains(self.study)

#         numStir = hand.count_of(self.stir) if hasGreen else 0
#         numPayoff = hand.count_of(self.payoff)
#         hasKarn = hand.contains(self.karn)
#         tronFinders = hand.count_of(self.exmap) + hand.count_of(self.sylv) if hasGreen else 0
#         numLand = hand.count_of(self.land_value_list)
#         numCantrips = hand.count_of(self.cantrips) + numStir
#         hasOStone = hand.contains(self.ostone)

        theNuts = False
        strongLedAndLoot = False
        weakLedAndLoot = False
        strongThreeLootAndDredge = False
        weakThreeLootAndDredge = False
        threeLootNoDredge = False
        twoLootAndDredge = False

        if ( hasLed and hasGoodDredgerOrMoreThanOne and 
        ((hasBlue and (hasBlueLoot) and hasLooting) or (hasGold and hasLooting)) ):
            theNuts = True
        
        #same as the nuts but weak dredger
        elif ( hasLed and hasDredge and 
        ((hasBlue and (hasBlueLoot) and hasLooting) or (hasGold and hasLooting)) ):
            strongLedAndLoot = True

        #the nuts without a loot and has a pimp
        elif ( hasLed and hasGoodDredgerOrMoreThanOne and 
        (hasBlue and (hasBlueLoot) and (hasGold and hasPimp)) ):
            strongLedAndLoot = True

        #all in on LED study with decent dredger
        elif ( hasLed and hasGoodDredgerOrMoreThanOne and 
        (hasBlue and (hasBlueLoot)) ):
            weakLedAndLoot = True

        #all in on LED with thug
        elif ( hasLed and hasDredge and 
        (hasBlue and (hasBlueLoot)) ):
            weakLedAndLoot = True

        #has a dredger 2 lands and 3 or 2 loot and a coliseum
        elif ( hasDredge and 
        (combinedNumPimpLoot > 2 and goldCount > 1) or (combinedNumPimpLoot > 1 and goldCount > 0 and hasColiseum) ):
            strongThreeLootAndDredge = True

        #has a dredger 2 lands and 3 or 2 loot and only 1 land
        elif ( hasDredge and 
        (combinedNumPimpLoot > 2 and goldCount == 1)):
            weakThreeLootAndDredge = True

        #has at least 1 land and 3 loots or 2 loots and land and coliseum
        elif((combinedNumPimpLoot > 2) or (combinedNumPimpLoot > 1 and hasColiseum)) and goldCount > 0 :
            threeLootNoDredge = True

        #has at least 1 land and 2 loots or 1 loots and land and coliseum
        elif((combinedNumPimpLoot > 1) or (combinedNumPimpLoot > 0 and hasColiseum)) and goldCount > 0 :
            twoLootAndDredge = True

        results = np.array([theNuts, strongLedAndLoot, weakLedAndLoot, strongThreeLootAndDredge, weakThreeLootAndDredge, threeLootNoDredge, twoLootAndDredge])
        #results = np.array([t3karnGG, tronWPayoff, justTron, keepable])
        #print(str (results))
        return results

if __name__ == "__main__":
    dredgeMullTester = DredgeMullTester()
    dredgeMullTester.run() 