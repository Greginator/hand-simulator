def output_results(output_file, iterations, mullto, p_good, hand_types, p_hands, p_early_success, p_success):
    with open(output_file,"w") as file:
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