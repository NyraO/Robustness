def deletion(r_file, strength, w_file):
    #strength is an integer and decides after which amount of words a word is not used
    #strenght of one deletes every word

    #reading original
    with open(r_file, 'r') as file:
        txt_list = file.read().splitlines()

    #creating new file for manipulated text
    open(w_file, 'x')

    #count used for skipping words (deletion)
    count = 0

    #iterating over every line and word in that line
    for string in txt_list:
        for word in string.split():

            if (count % strength) != 0:
                #writing unskipped words in new file
                with open(w_file, 'a') as f:
                    f.write(word+" ")
            count += 1





