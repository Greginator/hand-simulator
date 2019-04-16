import numpy as np
from hand import Hand
import resultwriter

iterations = 500000
starting_size = 7 #inclusive
mullto = 3	#not inclusive
hand_types = ["Tron", "Chalice + 2 Lands", "t3 TKS", "t2 Reshaper", "2 Temples + Spell"]
hand = Hand("decklists/e_tron.txt")
success = 0.0
early_success = 0.0
good_counts = np.zeros((starting_size + 1) - mullto)
hand_counts = np.zeros(((starting_size + 1) - mullto,len(hand_types)))
totals = np.zeros((starting_size + 1) - mullto)

land_names = ["Cavern of Souls", "Sea Gate Wreckage", "Wastes", "Eldrazi Temple", "Urza's Mine", "Urza's Power Plant", "Urza's Tower", "Ghost Quarter"]

for i in range(iterations):
	if i % 1000 == 0:
		print(str(i) + " of " + str(iterations))
	flag = False
	early_flag = False
	for j in range(0,(starting_size + 1) - mullto):
		hand.new_hand(starting_size - j)

		tron = hand.has_tron()
		lands = hand.count_of(land_names)
		has_TKS = hand.contains("Thought-Knot Seer")
		has_Reshaper = hand.contains("Matter Reshaper")
		has_Chalice = hand.contains("Chalice of the Void")
		temples = hand.count_of("Eldrazi Temple") 
		has_Map = float(hand.count_of("Expedition Map") > 0 and lands >= 2)
		has_Stone = hand.contains("Mind Stone")

		t3_TKS = has_TKS * (((has_Map or (temples > 0)) * (lands >= 2)) or (has_Stone * (lands >= 3)))
		# tron, Chalice + lands, t3 TKS, t2 Reshaper, 2 temples and any spell
		results = np.array([tron, has_Chalice * (lands >= 2), t3_TKS, has_Reshaper * (temples > 0) * (lands >= 2), (temples + has_Map*(lands >= 2) >= 2) * (lands < (7 - j))])
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

resultwriter.output_results("output/etron_output.csv", iterations, mullto, p_good, hand_types, p_hands, p_early_success, p_success)

print(p_good)
print(np.flip(p_hands, axis = 0))
print(p_early_success)
print(p_success)