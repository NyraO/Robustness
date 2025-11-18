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
