from abc import ABC, abstractmethod
import numpy as np

class MulliganTester(ABC):
    def __init__(self):
        self.iterations = 100000
        self.starting_size = 7
        self.mullto = 5
        self.resetCounters()

    @property
    @abstractmethod
    def output_file_header(self):
        pass

    @property
    @abstractmethod
    def hand(self):
        pass

    @property
    @abstractmethod
    def hand_types(self):
        pass

    @abstractmethod
    def CheckHand(self):
        pass

    def run(self):
        self.runLondon()
        self.printResults("London")
        self.runParis()
        self.printResults("Paris")
        self.runVancouver()
        self.printResults("Vancouver")

    def resetCounters(self):
        self.success = 0.0
        self.successAfterDraw = 0
        self.improvement_after_draw = [0] * (self.starting_size - self.mullto +1)
        self.good_counts = np.zeros((self.starting_size + 1) - self.mullto)
        self.hand_counts = np.zeros(((self.starting_size + 1) - self.mullto, len(self.hand_types)))
        self.totals = np.zeros((self.starting_size + 1) - self.mullto)

        self.good_counts_afterdraw = np.zeros((self.starting_size + 1) - self.mullto)
        self.hand_counts_afterdraw = np.zeros(((self.starting_size + 1) - self.mullto, len(self.hand_types)))

    def runParis(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))

            foundKeeper = False
            keeperAfterDraw = False
            for j in range(0,(self.starting_size + 1) - self.mullto):
                self.hand.new_hand(self.starting_size - j)

                results = self.CheckHand()
                
                self.hand.draw_card()
                resultAfterDraw = self.CheckHand()

                improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)

                self.good_counts[self.starting_size - j - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[self.starting_size - j - self.mullto,:] += results

                self.good_counts_afterdraw[self.starting_size - j - self.mullto] += (np.sum(resultAfterDraw) > 0)
                self.hand_counts_afterdraw[self.starting_size - j - self.mullto,:] += resultAfterDraw

                self.totals[self.starting_size - j - self.mullto] += 1
                self.improvement_after_draw[j] += improvedAfterDraw
                if not foundKeeper and np.sum(results) > 0:
                    foundKeeper = True
                if not keeperAfterDraw and np.sum(resultAfterDraw) > 0:
                    keeperAfterDraw = True
            self.successAfterDraw += keeperAfterDraw

            self.success += foundKeeper

    def getBestResult(self, results):
        best = None
        bestIndex = None
        for res in results:
            if True in res:
                if best is None:
                    best = res
                    bestIndex = np.argmax(best)
                    if bestIndex == 0:
                        break
                else:
                    testIndex = np.argmax(res)
                    if testIndex < bestIndex:
                        best = res
        if best is None:
            best = results[0]
        return best

    def runLondon(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))
            foundKeeper = False
            keeperAfterDraw = False
            for j in range(0,(self.starting_size + 1) - self.mullto):
                self.hand.new_hand(self.starting_size)
                if j > 0:
                    subResults = []
                    self.hand.generate_subset_hands(j)
                    for k in range(0, self.hand.num_subsets):
                        self.hand.nextSubset()
                        subResults.append(self.CheckHand())
                    results = self.getBestResult(subResults)
                else:
                    results = self.CheckHand()

                self.hand.draw_card()
                resultAfterDraw = self.CheckHand()

                improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)

                self.good_counts[self.starting_size - j - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[self.starting_size - j - self.mullto,:] += results

                self.good_counts_afterdraw[self.starting_size - j - self.mullto] += (np.sum(resultAfterDraw) > 0)
                self.hand_counts_afterdraw[self.starting_size - j - self.mullto,:] += resultAfterDraw

                self.totals[self.starting_size - j - self.mullto] += 1
                self.improvement_after_draw[j] += improvedAfterDraw
                if not foundKeeper and np.sum(results) > 0:
                    foundKeeper = True
                if not keeperAfterDraw and np.sum(resultAfterDraw) > 0:
                    keeperAfterDraw = True
            self.successAfterDraw += keeperAfterDraw
            self.success += foundKeeper

    def runVancouver(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))

            foundKeeper = False
            keeperAfterDraw = False
            for j in range(0,(self.starting_size + 1) - self.mullto):
                self.hand.new_hand(self.starting_size - j)

                results = self.CheckHand()

                self.hand.draw_card()
                resultAfterDraw = self.CheckHand()

                improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)
                if j is not 0 and not improvedAfterDraw:
                    #Replace the card drawn in the last operation
                    self.hand.scry_bottom()
                    resultAfterDraw = self.CheckHand()
                    improvedAfterDraw = self.checkImprovement(results, resultAfterDraw)
                
                self.good_counts[self.starting_size - j - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[self.starting_size - j - self.mullto,:] += results

                self.good_counts_afterdraw[self.starting_size - j - self.mullto] += (np.sum(resultAfterDraw) > 0)
                self.hand_counts_afterdraw[self.starting_size - j - self.mullto,:] += resultAfterDraw

                self.totals[self.starting_size - j - self.mullto] += 1
                self.improvement_after_draw[j] += improvedAfterDraw
                if not foundKeeper and np.sum(results) > 0:
                    foundKeeper = True
                if not keeperAfterDraw and np.sum(resultAfterDraw) > 0:
                    keeperAfterDraw = True
            self.successAfterDraw += keeperAfterDraw
            self.success += foundKeeper

    def checkImprovement(self, resultBeforeDraw, resultAfterDraw):
        if True in resultAfterDraw:
            bestNewRating = np.argmax(resultAfterDraw)
            bestOldRating = np.argmax(resultBeforeDraw)
            return bestNewRating < bestOldRating
        else:
            return False

    def printResults(self, header):
        p_good = self.good_counts / self.totals
        p_hands = self.hand_counts / self.totals.reshape((self.starting_size + 1) - self.mullto,1)
        p_success = self.success / self.iterations
        p_successAfterDraw = self.successAfterDraw / self.iterations
        p_drawImprovement = [x / self.iterations for x in self.improvement_after_draw]

        p_goodAfterDraw = self.good_counts_afterdraw / self.totals
        p_hands_afterDraw = self.hand_counts_afterdraw / self.totals.reshape((self.starting_size + 1) - self.mullto,1)

        print(p_good)
        print(np.flip(p_hands, axis = 0))
        print(p_drawImprovement)
        print(p_success)

        filename = "output/" + self.output_file_header + "_" + header+".csv"
        with open(filename, "w") as file:
            file.write(header + " - ")
            file.write(str(self.iterations) + " iterations\n\n")

            self.writeHandTypesToFile(file, p_good, p_hands)

            file.write("\n\nAfter Draw""\n")
            self.writeHandTypesToFile(file, p_goodAfterDraw, p_hands_afterDraw)

            file.write("\n")
            file.write("p of good hand by 5\n")
            file.write(str(p_success) + "\n")
            file.write("p of improvement after draw\n")
            file.write("7,6,5\n")
            file.write(str(p_drawImprovement) + "\n")
            file.write("p of good hand after draw\n")
            file.write(str(p_successAfterDraw) + "\n")
            file.close()


    def writeHandTypesToFile(self, file, p_good, p_hands):
        file.write("Probabilities of good hands:\n")
        for size in range(self.mullto,8):
            file.write(str(size) + ",")
        file.write("\n")
        for p in p_good:
            file.write(str(p) + ",")
        file.write("\n\n")

        # hand type headers
        file.write("hand sizes/types,")
        for type in self.hand_types:
            file.write(str(type) + ",")

        #results
        file.write("\n")
        for size in reversed(range(len(p_hands))):
            file.write(str(size + self.mullto) + ",")
            for p in p_hands[size,:]:
                file.write(str(p) + ",")
            file.write("\n")