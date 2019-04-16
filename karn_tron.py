import numpy as np
from hand import Hand
import resultwriter

iterations = 500000
starting_size = 7 #inclusive
mullto = 4	#not inclusive
hand_types = ["T3KarnGG", "Tron+payoff", "Tron", "solid_keep"]
hand = Hand("decklists/karn_tron.txt")
success = 0.0
early_success = 0.0
good_counts = np.zeros((starting_size + 1) - mullto)
hand_counts = np.zeros(((starting_size + 1) - mullto,len(hand_types)))
totals = np.zeros((starting_size + 1) - mullto)

green_source = ["Forest", "Chromatic Sphere", "Chromatic Star"]
tron1 = ["Urza's Power Plant"]
tron2 = ["Urza's Tower"]
tron3 = ["Urza's Mine"]
stir = ["Ancient Stirrings"]
sylv = ["Sylvan Scrying"]
exmap = ["Expedition Map"]
payoff = ["Walking Ballista", "Karn Liberated", "Wurmcoil Engine"]
karn = ["Karn Liberated"]
lands = ["Wastes", "Forest", "Urza's Power Plant", "Urza's Tower", "Urza's Mine"]
cantrips = ["Chromatic Sphere", "Chromatic Star", "Relic of Progenitus"]

def CheckHand(hand):
    #print("")
    #print (hand.hand_as_str())
    numTron = hand.contains(tron1) + hand.contains(tron2) + hand.contains(tron3)
    hasGreen = hand.contains(green_source)
    numStir = hand.count_of(stir) if hasGreen else 0
    numPayoff = hand.count_of(payoff)
    hasKarn = hand.contains(karn)
    tronFinders = hand.count_of(exmap) + hand.count_of(sylv) if hasGreen else 0
    numLand = hand.count_of(lands)
    numCantrips = hand.count_of(cantrips) + numStir

    t3karnGG = False
    tronWPayoff = False
    justTron = False
    keepable = False

    if numTron >= 1 and numLand >= 2 and numTron + tronFinders >= 3:
        if hasKarn:
            t3karnGG = True
        elif numPayoff > 0:
            tronWPayoff = True
        else:
            justTron = True
    elif numLand >= 2 and numCantrips >= 2 and numPayoff >= 1 and numPayoff < 4:
        keepable = True
    elif numLand >= 1 and numCantrips > 2:
        keepable = True

    results = np.array([t3karnGG, tronWPayoff, justTron, keepable])
    #print(str (results))
    return results

for i in range(iterations):
    if i % 5000 == 0:
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

resultwriter.output_results("output/karntron_output.csv", iterations, mullto, p_good, hand_types, p_hands, p_early_success, p_success)

print(p_good)
print(np.flip(p_hands, axis = 0))
print(p_early_success)
print(p_success)