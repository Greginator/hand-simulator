import numpy as np
from hand import Hand

iterations = 500000
starting_size = 7 #inclusive
mullto = 2	#not inclusive
hand_types = ["2 Lands Dredge 2 Discard", "2 Lands Dredge Discard", "2 Lands Faithless 2 Creatures",
"1 Land Dredge Faithless", "2 lands looting discard creature"]
hand = Hand("decklists/legacy_dredge.txt")
success = 0.0
early_success = 0.0
good_counts = np.zeros((starting_size + 1) - mullto)
hand_counts = np.zeros(((starting_size + 1) - mullto,len(hand_types)))
totals = np.zeros((starting_size + 1) - mullto)

land_names = ["mana confluence",
"gemstone mines",
"cephalid coliseum",
"city of brass"]

green_source = ["Wooded Foothills",
"Copperline Gorge",
"Bloodstained Mire",
"Stomping Ground",
"Gemstone Mine"]

discard = ["Insolent Neonate",
"Faithless Looting",
"Cathartic Reunion"
]

good_dredge = ["Stinkweed Imp",
"Golgari Thug"
]

ok_dredge = ["Life From The Loam",
"Darkblast"
]

dredge = ["Stinkweed Imp",
"Golgari Thug",
"Life From The Loam",
"Darkblast"
]

creature = [
"Prized Amalgam",
"Bloodghast"
]

for i in range(iterations):
	flag = False
	early_flag = False
	for j in range(0,(starting_size + 1) - mullto):
		hand.new_hand(starting_size - j)

		lands = hand.count_of(land_names)
		has_green = hand.contains(green_source)
		has_discard = hand.contains(discard)
		discard_count = hand.count_of(discard)
		has_dredge = hand.contains(dredge)
		has_creature = hand.contains(creature)
		has_faithless = hand.contains("Faithless Looting")
		has_faithless_and_2_creature = float(has_faithless and lands >= 2 and (hand.count_of("Bloodghast")>1 or (hand.count_of("Bloodghast") > 0 and hand.count_of("Prized Amalgam") > 0)))
		two_lands_1_green = (lands >= 2) * has_green
		#"2 Lands Dredge 2 Discard", "2 Lands Dredge Discard", "2 Lands Faithless 2 Creatures", "1 Land Dredge Faithless", "2 lands looting discard creature"
		results = np.array([two_lands_1_green * has_dredge * float(discard_count >= 2), two_lands_1_green *  has_dredge * has_discard, two_lands_1_green * has_faithless_and_2_creature, has_faithless * has_green * has_dredge, two_lands_1_green * has_faithless * float(discard_count >= 2) * has_creature  ])
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

with open("output/dredge_output.csv","w") as file:
	file.write(str(iterations) + " iterations\n\n")

	file.write("Probabilities of good hands:\n")
	for size in range(mullto,8):
		file.write(str(size) + ",")
	file.write("\n")
	for p in p_good:
		file.write(str(p) + ",")
	file.write("\n\n")

	# hand type headers
	file.write("hand sizes/types,")
	for type in hand_types:
		file.write(str(type) + ",")

	#results
	file.write("\n")
	for size in reversed(range(len(p_hands))):
		file.write(str(size + mullto) + ",")
		for p in p_hands[size,:]:
			 file.write(str(p) + ",")
		file.write("\n")

	file.write("\n")
	file.write("p of good hand by 5\n")
	file.write(str(p_early_success) + "\n")
	file.write("p of good hand by 3\n")
	file.write(str(p_success) + "\n")
	file.close()

print(p_good)
print(np.flip(p_hands, axis = 0))
print(p_early_success)
print(p_success)
