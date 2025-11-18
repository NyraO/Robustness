#Copy paste , insertion, and adding Noise
import random
import math

def tokenizer(text):
    return text.split(" ")

# prepare a 1500 word essay, watermarked text word count
# my parameter is dilution = 0.2; watermarked text word count = 100 words. 
# If dilution = 0.2 and watermarked text = 100 words, then:
# Total final text = 100 / 0.2 = 500 words
# Non-watermarked text added = 500 - 100 = 400 words
def copy_paste_attack(watermarked_text, dilution, excerpt):
    # excerpt is any text from the internet written before the time of LLMs
    excerpt_tokenized = tokenizer(excerpt)
    len_excerpt = len(excerpt_tokenized)

    watermarked_text_tokenized = tokenizer(watermarked_text)
    len_watermarked_text = len(watermarked_text_tokenized)

    final_text_size = math.ceil(len_watermarked_text / dilution)
    len_needed_text = final_text_size - len_watermarked_text

    cropped_excerpt = " ".join(excerpt_tokenized[0:len_needed_text+1]) 
    return cropped_excerpt + watermarked_text


# ratio input = inserted_word_count / input_file_word_count 
# ratio = 0.2, 400 * 0.2 = 80 words to be inserted
def insertion_attack(watermarked_text, ratio, words):
    watermarked_text_tokenized = tokenizer(watermarked_text)

    len_watermarked_text = len(watermarked_text_tokenized)
    len_words_to_add = math.ceil(len_watermarked_text * ratio)

    random_positions = []
    for i in range(len_words_to_add):
        pos = random.randrange(0, len_watermarked_text)
        random_positions.append(pos)

    for pos in random_positions:
        watermarked_text_tokenized.insert(pos, random.choice(words))
    
    return " ".join(watermarked_text_tokenized)


def insert_noise_attack(watermarked_text, ratio, punctuations=[",",":"]):
    watermarked_text_tokenized = tokenizer(watermarked_text)

    len_watermarked_text = len(watermarked_text_tokenized)
    len_words_to_add = math.ceil(len_watermarked_text * ratio)

    random_positions = []
    for i in range(len_words_to_add):
        pos = random.randrange(0, len_watermarked_text)
        random_positions.append(pos)

    for pos in random_positions:
        x = random.randrange(1,4)
        if x == 1:
            # add punctionations in random places
            punc = random.choice(punctuations)
            watermarked_text_tokenized[pos] += punc
        elif x == 2:
            # delete a letter
            select_word = watermarked_text_tokenized[pos]
            index_to_delete = random.randrange(0, len(select_word))
            removed_word = select_word[:index_to_delete] + select_word[index_to_delete+1:]
            watermarked_text_tokenized[pos] = removed_word
        else:
            # add a letter
            select_word = watermarked_text_tokenized[pos]
            insert_index = random.randrange(0, len(select_word))
            vowels = ["a", "e", "i", "o", "u"]
            modified_word = select_word[:insert_index] + random.choice(vowels) + select_word[insert_index+1:]
            watermarked_text_tokenized[pos] = modified_word
    
    return " ".join(watermarked_text_tokenized)


print(copy_paste_attack("The sky ​ appears blue ​ because molecules ​ in ​ the ​ atmosphere scatter ​ sunlight, and blue ​ light ​ is scattered ​ more strongly.", 
                        0.4, 
                        "excerpt"))