import numpy as np
from hand import Hand
import resultwriter

iterations = 500000
starting_size = 7
mullto = 4
hand_types = ["theNutz","good_mix","landsAndSpells"]
hand = Hand("decklists/gbRock.txt")
success = 0.0
early_success = 0.0
good_counts = np.zeros((starting_size + 1) - mullto)
hand_counts = np.zeros(((starting_size + 1) - mullto, len(hand_types)))
totals = np.zeros((starting_size + 1) - mullto)

multiSources = ["Blooming Marsh", "Overgrown Tomb", "Verdant Catacombs", "Twilight Mire", "Hissing Quagmire"]
blackSource = ["Swamp"]
greenSource = ["Forest", "Treetop Village"]
otherLand = ["Field of Ruin"]

earlyThreat = ["Dark Confidant", "Tarmogoyf", "Scavenging Ooze"]
interaction = ["Thoughtseize", "Inquisition of Kozilek", "Fatal Push"]
lili = ["Liliana of the Veil"]

def CheckHand(hand):
    #print("")
    #print (hand.hand_as_str())

    numLands = hand.count_of(multiSources) + hand.count_of(blackSource) + hand.count_of(greenSource) + hand.count_of(otherLand)
    hasGreen = hand.contains(multiSources) or hand.contains(greenSource)
    hasBlack = hand.contains(multiSources) or hand.contains(blackSource)
    numEarlyThreat = hand.count_of(earlyThreat)
    numInteraction = hand.count_of(interaction)
    hasLili = hand.contains(lili)

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

resultwriter.output_results("output/gbRock_output.csv", iterations, mullto, p_good, hand_types, p_hands, p_early_success, p_success)

print(p_good)
print(np.flip(p_hands, axis = 0))
print(p_early_success)
print(p_success)