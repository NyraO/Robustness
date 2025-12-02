import math

def tokenizer(text):
    return text.split(" ")

# copy_paste_attacks
#A  watermarked text is inserted into a larger corpus of unwatermarked text, diluting the watermark’s statistical signal


#input : watermarked text, unwatermarked text, percentage of dilution (What fraction of the final text is watermarked)
def copy_paste_attacks (watermarked_text, excerpt, dilution_rate, position):
    #len_total_text = (len(watermarked_text)) / dilution_rate
    #size_of_excerpt = len_total_text - len(watermarked_text) #the watermark needs to make up 20% of the final text
    #cropped_excerpt = excerpt [0:size_of_of_excerpt]
    
    size_of_watermarked_text= len(tokenizer(watermarked_text))
    len_total_text = math.ceil(size_of_watermarked_text) / dilution_rate)
    size_of_excerpt = len_total_text - len(tokenizer(watermarked_text))
    tokenized_excerpt = tokenizer(excerpt)
    cropped_excerpt = " ".join(tokenized_excerpt[0:size_of_excerpt]) 
    #final_text = watermarked_text + " " + cropped_excerpt
    text_to_be_replaced = cropped_excerpt.slice[position, position + size_of_watermarked_text]
    final_text = cropped_excerpt.replace(text_to_be_replaced, watermarked_text, size_of_watermarked_text)
    
    return final_text