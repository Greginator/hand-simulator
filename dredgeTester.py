from hand import Hand
from collections import Counter

#Test the hit rate of Dredgers
#We assume 7 cards have been drawn and then measure:
# 1) If we can trigger Winota
# 2) Whether Winota would hit a human
# 3) If Winota hits a human AND we can trigger her

class DredgeTester:
    def __init__(self):
        self.hand = Hand("decklists/led_dredge.txt")


        self.iterations = 100000

        #self.cardsDrawn = 7

        #dredges per breakthrough
        self.dredgesDone = 0
        #total dredges for all iterations
        self.dredgesDoneCounter = 0
        #total number of cards dredged
        self.cardsDredged = 0
        #number of times dredge chain ends at the first dredge
        self.brickCounter = 0
        #number of times dredge chain fully completes
        self.nutCounter = 0

        self.dredgers = ["Golgari Grave-Troll", "Stinkweed Imp", "Golgari Thug"]
        #Important: ordered from best to worst
        self.dredgeCounts = {
            "Golgari Grave-Troll": 6,
            "Stinkweed Imp": 5,
            "Golgari Thug": 4
        }

        self.dredgedCardNames = list()

        self.graveyard = set()

    def doDredge(self, dredger):
        for i in range(self.dredgeCounts[dredger]):
            self.graveyard.add(self.hand.draw_card())

        self.cardsDredged = self.cardsDredged + self.dredgeCounts[dredger]
        self.dredgesDone += 1
        self.dredgedCardNames.append(dredger)
    
    def getBestDredgerInGraveyard(self):
        #Counter([self.deck[i] for i in self.graveyard])
        graveyardCounter = Counter([self.hand.deck[i] for i in self.graveyard])
        #print(graveyardCounter)
        for dredgerName in self.dredgeCounts:
            if(graveyardCounter[dredgerName]):
                return dredgerName
        
        return False

    def removeDredgerFromGraveyard(self, dredgerName):
        for i in self.graveyard:
            if self.hand.deck[i] == dredgerName:
                self.graveyard.remove(i)
                return

    def reset(self):
        #reset this stuff
        self.dredgesDone = 0
        self.dredgedCardNames = list()
        self.graveyard = set()

    def run(self):
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))
            
            self.reset()

            #set the initial hand
            self.hand.new_hand(0)
            #draw a breakthrough
            self.hand.draw_card(1)
            #draw a grave troll
            self.hand.draw_card(26)
            #draw a golgari thug
            #self.hand.draw_card(30)
            self.hand.draw_card(2)
            self.hand.draw_card(3)
            self.hand.draw_card(4)
            self.hand.draw_card(5)
            self.hand.draw_card(6)
            #print(self.hand.card_counts)

            #always does 1 dredge to start so number of dredges will be 1+this val
            performDredgeCount = 3

            self.doDredge("Golgari Grave-Troll")
            bestDredgerName = self.getBestDredgerInGraveyard()
            #print(bestDredgerName)
            #print("grave counter")
            #print(Counter([self.hand.deck[i] for i in self.graveyard]))
            j = 0

            #print(bestDredgerName)
            #print(j)
            #print("breakthrough!!!!")
            while(bestDredgerName and j < performDredgeCount):
                #print("gone into the continue loop!!!")
                self.removeDredgerFromGraveyard(bestDredgerName)
                self.doDredge(bestDredgerName)
                bestDredgerName = self.getBestDredgerInGraveyard()
                #print("the best dredge was")
                #print(bestDredgerName)
                j = j + 1

            #if it only performs the first dredge
            if j==0:
                self.brickCounter += 1

            if j==performDredgeCount:
                self.nutCounter += 1

            self.dredgesDoneCounter += self.dredgesDone

        self.printResults()
    
    def printResults(self): 
        print("Trials " + str(self.iterations))

        averageCardsDredged = self.cardsDredged / self.iterations
        averageDredges = self.dredgesDoneCounter / self.iterations
        print ("All Complete Dredge Chains: " + str(self.nutCounter) + " All Complete Bricked Chains: " + str(self.brickCounter))
        percentageCompleted = (self.nutCounter/self.iterations)*100
        percentageBricked = (self.brickCounter/self.iterations)*100
        print ("Completed chain %: " + str(percentageCompleted) + " Bricked Chain %: " + str(percentageBricked))

        print("average Number of Dredges: " + str(averageDredges)+ " Average Cards Dredged: " + str(averageCardsDredged))

if __name__ == "__main__":
    dredgeTester = DredgeTester()
    dredgeTester.run() 