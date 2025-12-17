import math
import random
def tokenizer(text):
    return text.split(" ")

# copy_paste_attacks
#A  watermarked text is inserted into a larger corpus of unwatermarked text, diluting the watermark’s statistical signal
#Insert watermarked text into excerpt at specified position


def copy_paste_attack(watermarked_text, excerpt, dilution_rate, position):

    wm_tokens = tokenizer(watermarked_text)
    excerpt_tokens = tokenizer(excerpt)
    
    
    size_watermarked = len(wm_tokens)
    total_size_needed = math.ceil(size_watermarked / dilution_rate)
    size_excerpt_needed = total_size_needed - size_watermarked
    
    
    cropped_tokens = excerpt_tokens[:size_excerpt_needed]
    
   
    before_tokens = cropped_tokens[:position]
    after_tokens = cropped_tokens[position + size_watermarked:]
    
   
    final_tokens = before_tokens + wm_tokens + after_tokens
    
    
    final_text = " ".join(final_tokens)
    
    return final_text


# print(copy_paste_attack ("long watermarked_text", "" \
# "Tom he made a sign to me kind of a little noise with his mouth and we" \
# "went creeping away on our hands and knees. When we was ten foot off" \
# "Tom whispered to me, and wanted to tie Jim to the tree for fun. But I" \
# "said no; he might wake and make a disturbance, and then they’d find out" \
# "I warn’t in. Then Tom said he hadn’t got candles enough, and he would" \
# "slip in the kitchen and get some more. I didn’t want him to try. I said" \
# "Jim might wake up and come. But Tom wanted to resk it; so we slid in" \
# "there and got three candles, and Tom laid five cents on the table for" \
# "pay. Then we got out, and I was in a sweat to get away; but nothing" \
# "would do Tom but he must crawl to where Jim was, on his hands and" \
# "knees, and play something on him. I waited, and it seemed a good while," \
# "everything was so still and lonesome.", 0.2,3))



# insertion_attacks
#words or sentences are randomly added into the text to change the generated watermark
def insertion_attack(watermarked_text, ratio, words):

    tokens = tokenizer(watermarked_text)
    original_length = len(tokens)
    
    
    num_words_to_insert = math.ceil(original_length * ratio)
    
    random_positions = [random.randint(0, original_length) for _ in range(num_words_to_insert)]
    
    # Sort positions in REVERSE order (insert from end to beginning)
    # This way, earlier positions don't shift when we insert
    random_positions.sort(reverse=True)
    
    # Insert words at each position
    for pos in random_positions:
        word_to_insert = random.choice(words)
        tokens.insert(pos, word_to_insert)
    
    return " ".join(tokens)
# Test
watermarked = "The quick brown fox jumps"
word_bank = ["very", "extremely", "really", "absolutely"]

# result = insertion_attack(watermarked, ratio=0.4, words=word_bank)
# print(result)



def insert_noise_attack(watermarked_text, ratio, punctuations=[",", ":", ";"]):

  
    tokens = tokenizer(watermarked_text)
    len_watermarked_text = len(tokens)
    
    # Calculate how many words to modify
    num_words_to_modify = math.ceil(len_watermarked_text * ratio)
    
    # Generate UNIQUE random positions
    random_positions = random.sample(range(len_watermarked_text), 
                                     min(num_words_to_modify, len_watermarked_text))
    
    # Apply modifications
    for pos in random_positions:
        # Choose modification type randomly
        modification_type = random.randint(1, 3)
        
        if modification_type == 1:
            # Add punctuation to the word
            punc = random.choice(punctuations)
            tokens[pos] += punc
            
        elif modification_type == 2:
            # Delete a random letter from the word
            word = tokens[pos]
            if len(word) > 1:  # Only delete if word has more than 1 character
                index_to_delete = random.randrange(0, len(word))
                modified_word = word[:index_to_delete] + word[index_to_delete + 1:]
                tokens[pos] = modified_word
            
        else:  # modification_type == 3
            # Insert a random vowel into the word
            word = tokens[pos]
            if len(word) > 0:  # Only insert if word is not empty
                insert_index = random.randrange(0, len(word) + 1)  # +1 to allow appending
                vowels = ["a", "e", "i", "o", "u"]
                modified_word = word[:insert_index] + random.choice(vowels) + word[insert_index:]
                tokens[pos] = modified_word
    
    return " ".join(tokens)

text = "The quick brown fox jumps over the lazy dog"
# result = insert_noise_attack(text, ratio=0.3)
# print(result)
