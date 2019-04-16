import numpy as np
from hand import Hand
import resultwriter

iterations = 500000
starting_size = 7
mullto = 4
hand_types = ["#TheNutz", "stirNutz", "double amulet", "t3/4 titan", "solid keep"]
hand = Hand("decklists/amulet.txt")
success = 0.0
early_success = 0.0
good_counts = np.zeros((starting_size + 1) - mullto)
hand_counts = np.zeros(((starting_size + 1) - mullto, len(hand_types)))
totals = np.zeros((starting_size + 1) - mullto)

one_mana_lands = ["Forest", "Bojuka Bog", "Botanical Sanctum", "Cavern of Souls", "Gemstone Mine", "Kabira Crossroads", "Khalni Garden", "Slayers' Stronghold", "Sunhome, Fortress of the Legion", "Tolaria West"]
vesuva = ["Vesuva"]
bounce_lands = ["Boros Garrison", "Selesnya Sanctuary", "Simic Growth Chamber"]
green_source = ["Forest", "Botanical Sanctum", "Cavern of Souls", "Selesnya Sanctuary", "Simic Growth Chamber", "Gemstone Mine", "Khalni Garden"] 
amulet = ["Amulet of Vigor"]
ramp_dudes = ["Azusa, Lost but Seeking", "Sakura-Tribe Scout", "Coalition Relic"]
payoff = ["Hive Mind", "Primeval Titan", "Summoner's Pact", "Tolaria West"]
the_fat = ["Hive Mind", "Primeval Titan", "Walking Ballista", "Pact of Negation", "Summoner's Pact"]
stir = ["Ancient Stirrings"]
relic = ["Coalition Relic"]

def CheckHand(hand):
    #print("")
    #print (hand.hand_as_str())
    
    num_reg_land = hand.count_of(one_mana_lands)
    num_vesuva = hand.count_of(vesuva)
    num_bounce = hand.count_of(bounce_lands)
    land_mana = num_reg_land + 2*num_bounce + (num_vesuva if num_bounce == 0 else num_vesuva*2)
    num_green_source = hand.count_of(green_source)
    
    num_amulet = hand.count_of(amulet)  
    num_payoff = hand.count_of(payoff)
    num_stir = hand.count_of(stir)
    num_relic = hand.count_of(relic)
    num_ramp_dudes = hand.count_of(ramp_dudes)
    num_high_cc = hand.count_of(the_fat)

    num_mana = land_mana + (num_amulet if num_bounce > 1 else 0) + num_relic*2 + (1 if num_stir and num_green_source else 0)
    has_6_mana = land_mana >= 3 and num_mana >= 6
    nutz_count = 0
    nutz_count += num_amulet > 0
    nutz_count += num_ramp_dudes > 0
    nutz_count += num_reg_land > 0
    nutz_count += num_green_source > 0
    nutz_count += num_payoff > 0
    nutz_count += has_6_mana

    is_nutz = False
    stir_nutz = False
    double_amulet = False
    is_t4_titan = False
    solid_keep = False

    if nutz_count >= 6:
        is_nutz = True
    elif num_reg_land > 0 and num_green_source > 0 and nutz_count + num_stir >= 6:
        stir_nutz = True
    elif num_amulet > 1 and land_mana > 1 and (num_bounce > 0 or (num_green_source > 0 and num_reg_land > 0 and num_stir > 0)):
        double_amulet = True
    elif num_ramp_dudes > 0 and num_payoff > 0 and has_6_mana:
        is_t4_titan = True
    elif num_reg_land > 0 and num_green_source > 0 and nutz_count + num_stir >= 5 and num_high_cc < 3:
        solid_keep = True

    results = np.array([is_nutz, stir_nutz, double_amulet, is_t4_titan, solid_keep])
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

resultwriter.output_results("output/amulet_output.csv", iterations, mullto, p_good, hand_types, p_hands, p_early_success, p_success)

print(p_good)
print(np.flip(p_hands, axis = 0))
print(p_early_success)
print(p_success)