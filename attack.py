import math

def tokenizer(text):
    return text.split(" ")

# copy_paste_attacks
#A  watermarked text is inserted into a larger corpus of unwatermarked text, diluting the watermark’s statistical signal


#input : watermarked text, unwatermarked text, percentage of dilution (What fraction of the final text is watermarked)
def copy_paste_attacks (watermarked_text, excerpt, dilution_rate):
    #len_total_text = (len(watermarked_text)) / dilution_rate
    #size_of_excerpt = len_total_text - len(watermarked_text) #the watermark needs to make up 20% of the final text
    #cropped_excerpt = excerpt [0:size_of_of_excerpt]

    len_total_text = math.ceil(len(tokenizer(watermarked_text)) / dilution_rate)
    size_of_excerpt = len_total_text - len(tokenizer(watermarked_text))
    tokenized_excerpt = tokenizer(excerpt)
    cropped_excerpt = " ".join(tokenized_excerpt[0:size_of_excerpt]) 
    final_text = watermarked_text + " " + cropped_excerpt
    return final_text



print(copy_paste_attacks ("watermarked_text", "" \
"Tom he made a sign to me kind of a little noise with his mouth and we" \
"went creeping away on our hands and knees. When we was ten foot off" \
"Tom whispered to me, and wanted to tie Jim to the tree for fun. But I" \
"said no; he might wake and make a disturbance, and then they’d find out" \
"I warn’t in. Then Tom said he hadn’t got candles enough, and he would" \
"slip in the kitchen and get some more. I didn’t want him to try. I said" \
"Jim might wake up and come. But Tom wanted to resk it; so we slid in" \
"there and got three candles, and Tom laid five cents on the table for" \
"pay. Then we got out, and I was in a sweat to get away; but nothing" \
"would do Tom but he must crawl to where Jim was, on his hands and" \
"knees, and play something on him. I waited, and it seemed a good while," \
"everything was so still and lonesome.", 0.2))
  



# insertion_attacks
#words or sentences are randomly added into the text to change the generated watermark



# insert_noise_attacks