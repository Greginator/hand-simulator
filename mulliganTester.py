from abc import ABC, abstractmethod
import numpy as np

class MulliganTester(ABC):
    def __init__(self):
        self.iterations = 500000
        self.starting_size = 7
        self.mullto = 5
        self.resetCounters()

    @property
    @abstractmethod
    def output_file(self):
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

    def resetCounters(self):
        self.success = 0.0
        self.early_success = 0.0
        self.good_counts = np.zeros((self.starting_size + 1) - self.mullto)
        self.hand_counts = np.zeros(((self.starting_size + 1) - self.mullto, len(self.hand_types)))
        self.totals = np.zeros((self.starting_size + 1) - self.mullto)

    def runParis(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))

            flag = False
            early_flag = False
            for j in range(0,(self.starting_size + 1) - self.mullto):
                self.hand.new_hand(self.starting_size - j)

                results = self.CheckHand()
                
                self.good_counts[self.starting_size - j - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[self.starting_size - j - self.mullto,:] += results
                self.totals[self.starting_size - j - self.mullto] += 1
                if not flag:
                    if (np.sum(results) > 0):
                        flag = True
                        if(j <= 2):
                            early_flag = True
            self.success += flag
            self.early_success += early_flag

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
            flag = False
            early_flag = False
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
                
                self.good_counts[self.starting_size - j - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[self.starting_size - j - self.mullto,:] += results
                self.totals[self.starting_size - j - self.mullto] += 1
                if not flag:
                    if (np.sum(results) > 0):
                        flag = True
                        if(j <= 2):
                            early_flag = True
            self.success += flag
            self.early_success += early_flag

    def runVancouver(self):
        self.resetCounters()
        for i in range(self.iterations):
            if i % 5000 == 0:
                print(str(i) + " of " + str(self.iterations))

            flag = False
            early_flag = False
            for j in range(0,(self.starting_size + 1) - self.mullto):
                self.hand.new_hand(self.starting_size - j)

                results = self.CheckHand()
                
                self.good_counts[self.starting_size - j - self.mullto] += (np.sum(results) > 0)
                self.hand_counts[self.starting_size - j - self.mullto,:] += results
                self.totals[self.starting_size - j - self.mullto] += 1
                if not flag:
                    if (np.sum(results) > 0):
                        flag = True
                        if(j <= 2):
                            early_flag = True
            self.success += flag
            self.early_success += early_flag

    def output_results(self, p_good, p_hands, p_early_success, p_success, header):
        with open(self.output_file,"w") as file:
            file.write(header)
            file.write(str(self.iterations) + " iterations\n\n")

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

            file.write("\n")
            file.write("p of good hand by 5\n")
            file.write(str(p_early_success) + "\n")
            file.write("p of good hand by 3\n")
            file.write(str(p_success) + "\n")
            file.close()

    def printResults(self, header):
        p_good = self.good_counts / self.totals
        p_hands = self.hand_counts / self.totals.reshape((self.starting_size + 1) - self.mullto,1)
        p_early_success = self.early_success / self.iterations
        p_success = self.success / self.iterations

        self.output_results(p_good, p_hands, p_early_success, p_success, header)

        print(p_good)
        print(np.flip(p_hands, axis = 0))
        print(p_early_success)
        print(p_success)