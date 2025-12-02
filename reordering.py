import random
from random import randrange


def reorder(r_file, strength, distance, w_file):
    #strength for choosing words
    #distance for distance between original position and new position

    # reading original
    with open(r_file, 'r') as file:
        txt_list = file.read().splitlines()

    # creating new file for manipulated text
    open(w_file, 'x')

    # count used for skipping words (deletion)
    count = 0

    #dictionary to map specific counts to words
    marked = {}

    # iterating over every line and word in that line
    for string in txt_list:
        for word in string.split():

            #saving chosen words
            if (count % strength) == 0:
                marked[count]=word

            #unchosen words get added to file
            else:
                with open(w_file, 'a') as f:
                    f.write(word + " ")

            #creating speparate list for iteration -> else length changed while iterating
            for c in list(marked.keys()):

                # if enough distance cover -> saved words get added
                if (c+distance) == count:

                    with open(w_file, 'a') as f:
                        f.write(marked[c] + " ")
                    marked.pop(c)
                    
            count += 1

#reorder("bsp.txt", 3, 2, "bsp_reord.txt" )

def reorder_random(r_file, strength, distance, w_file):
    # strength for choosing amount of moved words
    # distance for distance between original position and new position

    # reading original
    with open(r_file, 'r') as file:
        txt_list = file.read().split()

    # creating new file for manipulated text
    open(w_file, 'x')

    count = 0

    # dictionary to map specific counts to words
    marked = {}

    rand = []
    i = 0

    if strength > len(txt_list):
        raise ValueError("strength must be <= number of lines")

    rand = random.sample(range(len(txt_list)), strength)

    # iterating over every line and word in that line
    for word in txt_list:

        # saving chosen words
        if count in rand:
            marked[count] = word

        # unchosen words get added to file
        else:
            with open(w_file, 'a') as f:
                f.write(word + " ")

        # creating speparate list for iteration -> else length changed while iterating
        for c in list(marked.keys()):

            # if enough distance cover -> saved words get added
            if (c + distance) == count:
                with open(w_file, 'a') as f:
                    f.write(marked[c] + " ")
                marked.pop(c)

        count += 1

    #adding words that never reached distance
    for c in sorted(marked.keys()):
        with open(w_file, 'a') as f:
            f.write(marked[c] + " ")

#reorder_random("bsp.txt", 3, 2, "bsp_reord_rand.txt" )

def reorder_random_max_dist(r_file, strength, max_distance, w_file):
    # strength for choosing amount of moved words
    # distance for distance between original position and new position

    # reading original
    with open(r_file, 'r') as file:
        txt_list = file.read().split()

    # creating new file for manipulated text
    open(w_file, 'x')

    count = 0

    # dictionary to map specific counts to words
    marked = {}

    rand = []
    i = 0

    if strength > len(txt_list):
        raise ValueError("strength must be <= number of lines")

    rand = random.sample(range(len(txt_list)), strength)

    # iterating over every line and word in that line
    for word in txt_list:

        # saving chosen words
        if count in rand:
            marked[count+(randrange(1, max_distance+1))] = word

        # unchosen words get added to file
        else:
            with open(w_file, 'a') as f:
                f.write(word + " ")

        # creating sepeparate list for iteration -> else length changed while iterating
        for c in list(marked.keys()):

            # if enough distance cover -> saved words get added
            if c == count:
                with open(w_file, 'a') as f:
                    f.write(marked[c] + " ")
                marked.pop(c)

        count += 1

    #adding words that never reached distance
    for c in sorted(marked.keys()):
        with open(w_file, 'a') as f:
            f.write(marked[c] + " ")

reorder_random_max_dist("bsp.txt", 3, 2, "bsp_reord_rand_max.txt" )