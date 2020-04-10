from hand import Hand

class WinotaTester:
    def __init__(self):
        self.hand = Hand("decklists/winota.txt")
        self.trials = 0
        self.castWinotaHits = 0
        self.noWinotaTrigger = 0
        self.castWinotaMiss = 0
        self.iterations = 1000000
        self.cardsDrawn = 10
        self.AllHits = 0

    def checkWinotaTrigger(self):
        winotaTrigger = []
        for i in range(6):
            winotaTrigger.append(self.hand.deck[self.hand.draw_card()])
        return 'human' in winotaTrigger

    def run(self):
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))
            self.trials += 1
            self.hand.new_hand(10)
            numLands = self.hand.count_of('land')
            winotaDrawn = self.hand.contains('winota')
            goblinDrawn = self.hand.contains('goblin')
            
            wouldHit = self.checkWinotaTrigger()
            if numLands < 4 or not winotaDrawn or not goblinDrawn:
                self.noWinotaTrigger += 1
            elif wouldHit:
                self.castWinotaHits += 1
            else:
                self.castWinotaMiss += 1
            
            if wouldHit:
                self.AllHits += 1
        self.printResults()
    
    def printResults(self): 
        print("Trials " + str(self.trials))
        misses = self.trials - self.AllHits
        hitRate = self.AllHits / self.trials
        print ("All Hits: " + str(self.AllHits) + " All Misses: " + str(misses) + " General Hit rate: " + str(hitRate))
        realHitRate = self.castWinotaHits / (self.castWinotaHits + self.castWinotaMiss)
        print ("Real Hits: " + str(self.castWinotaHits) + " Real Misses: " + str(self.castWinotaMiss) + " Real Hit rate: " + str(realHitRate))

if __name__ == "__main__":
    winotaTester = WinotaTester()
    winotaTester.run() 