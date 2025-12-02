import random
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

#deletion("bsp.txt", 3, "bsp_del.txt")


def delete_random(r_file, strength, w_file):
    # strength is an integer and decides the amount of words deleted from the text

    #reading original
    with open(r_file, 'r') as file:
        txt_list = file.read().split()

    # creating new file for manipulated text
    open(w_file, 'x')

    rand = []
    count = 0
    dele = 0
    i = 0

    # index von zu löschenden wörtern generieren
    rand = random.sample(range(len(txt_list)), strength)

    #sortieren der generierten indexen
    rand.sort()

    # alle wörter im text durchgehen
    for word in txt_list:
        # wenn wort bestimmten index hat, wird es gelöscht
        if (count == rand[dele]):
            if dele < strength-1:
                dele += 1
        else:
            with open(w_file, 'a') as f:
                f.write(word+" ")
        count += 1

#delete_random("bsp.txt", 3, "bsp_del_ran.txt" )

def delete_portion(r_file, begin, end, w_file):
    #begin and end determine where the deleted part begins and where it ends

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

            if (begin > count) or (count > end):
                #writing unskipped words in new file
                with open(w_file, 'a') as f:
                    f.write(word+" ")
            count += 1

delete_portion("bsp.txt", 1, 3, "bsp_del_part.txt")