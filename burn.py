import numpy as np
from hand import Hand
import resultwriter

iterations = 500000
starting_size = 7
mullto = 4
hand_types = ["twolandCreature","goodhand","keepable"]
hand = Hand("decklists/burn.txt")
success = 0.0
early_success = 0.0
good_counts = np.zeros((starting_size + 1) - mullto)
hand_counts = np.zeros(((starting_size + 1) - mullto, len(hand_types)))
totals = np.zeros((starting_size + 1) - mullto)

rwSources = ["Bloodstained Mire", "Inspiring Vantage", "Sacred Foundry", "Scalding Tarn", "Wooded Foothills"]
mountain = ["Mountain"]

oneDropC = ["Goblin Guide", "Grim Lavamancer", "Monastery Swiftspear"]

def CheckHand(hand):
    #print("")
    #print (hand.hand_as_str())

    numRW = hand.count_of(rwSources)
    numLands = numRW + hand.count_of(mountain)
    numEarlyThreat = hand.count_of(oneDropC)

    twolandCreature = False
    goodhand = False
    keepable = False

    if numLands == 2 and numRW >= 1 and numEarlyThreat >= 1:
        twolandCreature = True
    elif numLands > 1 and numLands/hand.handsize() <= 0.6:
        goodhand = True
    elif hand.handsize() < 7 and numLands == 1 and numEarlyThreat == 1:
        keepable = True

    results = np.array([twolandCreature, goodhand, keepable])
    #print(str (results))
    return results

for i in range(iterations):
    if i % 1000 == 0:
        print(str(i) + " of " + str(iterations))
    flag = False
    early_flag = False
    for j in range(0,(starting_size + 1) - mullto):
        hand.new_hand(starting_size - j)

        results = CheckHand(hand)

        good_counts[starting_size - j - mullto] += (np.sum(results) > 0)
        hand_counts[starting_size - j - mullto,:] += results
        totals[starting_size - j - mullto] += 1
        if not flag:
            if (np.sum(results) > 0):
                flag = True
                if(j <= 2):
                    early_flag = True
    success += flag
    early_success += early_flag

p_good = good_counts / totals
p_hands = hand_counts / totals.reshape((starting_size + 1) - mullto,1)
p_early_success = early_success / iterations
p_success = success / iterations

resultwriter.output_results("output/burn_output.csv", iterations, mullto, p_good, hand_types, p_hands, p_early_success, p_success)

print(p_good)
print(np.flip(p_hands, axis = 0))
print(p_early_success)
print(p_success)