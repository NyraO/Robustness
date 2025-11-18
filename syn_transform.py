from nltk import sent_tokenize

from act_pas import *

def syn_transform(r_file, strength, w_file):
    #strength for one of how many sentences used

    #reading out whole text file
    with open(r_file, 'r') as file:
        txt_list = file.read()

    #using nltk to split text into single sentences
    sentences = sent_tokenize(txt_list)

    #creating file for saving
    open(w_file, 'x')

    #count for amount of sentences changed
    count = 0

    #iterating over sentences
    for s in sentences:
        #changing sentences from active to passive
        if (count % strength) == 0:
            s_out = active_to_passive(s)

        else:
            s_out = s

        #no space before end of sentence
        s_out = re.sub(r'<.!?>', '', s_out)

        #space after end of sentence
        s_out = s_out.strip() + ' '

        #write sentence into new file
        with open(w_file, 'a') as f:
            f.write(s_out.capitalize())

        count += 1

