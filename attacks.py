#!/usr/bin/env python3
"""
=============================================================================
ATTACK ENGINE
=============================================================================
"""

import random
import warnings
import math
import re
from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk import sent_tokenize
from src.act_pas.act_pas import *
import torch
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM, GenerationConfig

warnings.filterwarnings('ignore')


def tokenizer(text):
    return text.split(" ")


def penn_to_wn_pos(penn_pos: str):
    """
    Convert Penn Treebank POS tags to WordNet POS tags
    """
    if penn_pos.startswith("N"):
        return wn.NOUN
    if penn_pos.startswith("V"):
        return wn.VERB
    if penn_pos.startswith("J"):
        return wn.ADJ
    if penn_pos.startswith("R"):
        return wn.ADV
    return None


def get_synonym(word, wn_pos):
    synonyms = wn.synsets(word, pos=wn_pos)
    if not synonyms:
        return None
    candidates = []
    for i in synonyms:
        for lemma in i.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower():
                candidates.append(name)
    return random.choice(candidates) if candidates else None


class AttackEngine:

    @staticmethod
    def copy_paste_attack(watermarked_text, excerpt, dilution_rate, position):
        """
        A  watermarked text is inserted into a larger corpus of unwatermarked text, diluting the watermark’s
        statistical signal
        Insert watermarked text into excerpt at specified position
        """

        wm_tokens = tokenizer(str(watermarked_text))
        excerpt_tokens = tokenizer(str(excerpt))

        size_watermarked = len(wm_tokens)
        total_size_needed = math.ceil(size_watermarked / dilution_rate)
        size_excerpt_needed = max(total_size_needed - size_watermarked, 0)

        # Crop excerpt to required size
        cropped_tokens = excerpt_tokens[:size_excerpt_needed]

        # Handle empty excerpt case
        if not cropped_tokens:
            return " ".join(wm_tokens)

        position = max(0.0, min(1.0, float(position)))
        # Convert to token index
        insert_idx = int(position * len(cropped_tokens))
        # Ensure valid bounds
        insert_idx = min(insert_idx, len(cropped_tokens))
        # Insert watermarked tokens
        final_tokens = (cropped_tokens[:insert_idx] + wm_tokens + cropped_tokens[insert_idx:])

        final_text = " ".join(final_tokens)
        return final_text

    @staticmethod
    def insertion_attack(watermarked_text, ratio, words):
        """
        Words or sentences are randomly added into the text to change the generated watermark
        """

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

    @staticmethod
    def insert_noise_attack(watermarked_text, ratio, punctuations=None):
        if punctuations is None:
            punctuations = [",", ":", ";"]
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

    @staticmethod
    def deletion_attack(watermarked_text, strength):
        """
        Strength is an integer and decides the amount of words deleted from the text
        """

        txt_list = watermarked_text.split()

        # Normalize and convert to absolute count
        num_delete = int(strength * len(txt_list))
        if num_delete > len(txt_list)-4:
            num_delete=len(txt_list)-3

        if num_delete == 0:
            return watermarked_text

        num_delete = min(num_delete, len(txt_list))

        delete_indices = set(random.sample(range(len(txt_list)), num_delete))
        result = [word for i, word in enumerate(txt_list) if i not in delete_indices]

        return " ".join(result)

    @staticmethod
    def generative_attack(text, token, n):
        """
        Insert a specific token every n words
        """
        words = text.split()
        output_words = []
        for i in range(len(words)):
            output_words.append(words[i])
            if i % n == 0:
                output_words.append(token)
        
        return " ".join(output_words)

    @staticmethod
    def paraphrasing_attack(text, size=1.2, temperature=0.8):
        """
        Paraphrase a sentence using LLM
        """
        MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

        prompt = f"""
            You are a paraphrasing engine. Rewrite the the user's text while preserving meaning.
            Rules:
            - Do not shorten meaning
            - Do not add new ideas
            - Produce natural and fluent English
            """
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            dtype=torch.float16,
            device_map="auto",
            offload_folder=None
        )

        pipe = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer
        )

        input_tokens = tokenizer.encode(text, add_special_tokens=False)

        max_new_tokens = int(len(input_tokens) * size)

        messages = [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text}
        ]

        gen_config = GenerationConfig(
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=0.9,
            pad_token_id=tokenizer.eos_token_id
        )

        output = pipe(
            messages,
            generation_config=gen_config
        )
        return output[0]["generated_text"][-1]["content"].strip()

    @staticmethod
    def synonym_attack(text, replace_prob=0.2, max_replace_ratio=0.1, seed=None):
        """
        Paraphrase "watermarked text" randomly substituting words with synonyms
        """

        if seed is not None:
            random.seed(seed)
        tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)  # Tokenize with punctuation preserved
        words_only = [t for t in tokens if t.isalpha()]
        pos_tags = pos_tag(words_only)
        token_word_indices = [i for i, t in enumerate(tokens) if t.isalpha()]
        max_replacements = int(len(words_only) * max_replace_ratio)
        if max_replacements == 0:
            max_replacements = 1
        # positions of words to substitute with synonym
        candidate_word_positions = list(range(0, len(words_only), len(words_only) // max_replacements))[
                                   :max_replacements]
        replaced = 0
        for wpos in candidate_word_positions:
            if replaced >= max_replacements:
                break
            if random.random() > replace_prob:
                continue
            word, penn_pos = pos_tags[wpos]
            wn_pos = penn_to_wn_pos(penn_pos)
            if wn_pos is None:
                continue
            synonym = get_synonym(word, wn_pos)
            if synonym and synonym.lower() != word.lower():
                token_idx = token_word_indices[wpos]
                if word.isupper():
                    tokens[token_idx] = synonym.upper()
                else:
                    tokens[token_idx] = synonym.lower()
                replaced += 1
        return " ".join(tokens)

    @staticmethod
    def reorder_attack(text, strength, distance):
        """
        Strength for choosing amount of moved words
        distance for distance between original position and new position
        """
        txt_list = text.split()
        words = len(txt_list)

        # Normalize distance
        distance_tokens = int(distance * words)

        if strength > words:
            strength = words

        if strength == 0 or distance_tokens == 0:
            return text

        result = ""
        count = 0
        marked = {}

        rand = random.sample(range(words), strength)

        for word in txt_list:
            if count in rand:
                marked[count] = word
            else:
                result += word + " "

            for c in list(marked.keys()):
                if (c + distance_tokens) <= count:
                    result += marked[c] + " "
                    marked.pop(c)

            count += 1

        # Append remaining words
        for c in sorted(marked.keys()):
            result += marked[c] + " "

        return result.strip()

    @staticmethod
    def syn_transform_attack(text, strength):
        """
        Strength for one of how many sentences used
        """

        # using nltk to split text into single sentences
        sentences = sent_tokenize(text)
        num_transform = int(strength * len(sentences))
        chosen = set(random.sample(range(len(sentences)), num_transform))

        result = ""

        for i, s in enumerate(sentences):
            if i in chosen:
                s_out = active_to_passive(s)
            else:
                s_out = s
            # Clean spacing
            s_out = re.sub(r'\s+([.!?])', r'\1', s_out)
            result += s_out.strip() + " "

        return result.strip()

    @staticmethod
    def translation_attack(text, bridge_language='es'):
        """Translation attack: EN → bridge → EN"""
        try:
            from deep_translator import GoogleTranslator
            #languages = ['es', 'fr', 'de', 'it', 'pt', 'zh-CN', 'ja', 'ko', 'ru', 'ar']
            intermediate = GoogleTranslator(source='en', target=bridge_language).translate(text)
            back_translated = GoogleTranslator(source=bridge_language, target='en').translate(intermediate)
            return back_translated
        except Exception as e:
            return text

    def apply_attack(self, text: str, attack_type: str, params: dict = None) -> str:
        """Apply LLM-based attack to text"""

        if not text:
            return text
        params = params or {}

        print(f"Applying {attack_type} with params: {params}")

        try:
            if attack_type == 'copy_paste':
                dilution_rate = float(params.get('Dilution Rate', 0.3))
                position = float(params.get('Position', 1))
                excerpt = open("texts\\goethe.txt").read()
                return self.copy_paste_attack(text, excerpt, dilution_rate, position)

            elif attack_type == 'insert':
                coef = float(params.get('Coefficient', 0.3))
                filler_words = list(open("texts\\goethe.txt").read().split() * 10)
                return self.insertion_attack(text, coef, filler_words)

            elif attack_type == 'insert_noise':
                coef = float(params.get('Coefficient', 0.3))
                return self.insert_noise_attack(text, coef)

            elif attack_type == 'delete':
                coef = float(params.get('Coefficient', 0.3))
                return self.deletion_attack(text, coef)

            elif attack_type == 'generative':
                freq = int(params.get('Token Frequency', 5))
                freq = max(1, freq)
                return self.generative_attack(text, "😈".encode("utf-8-sig").decode("utf-8-sig"), freq)  # <extra>

            elif attack_type == 'synonym':
                max_ratio = float(params.get('Max Replace Ratio', 0.3))
                prob = float(params.get('Replace Probability', 0.5))
                return self.synonym_attack(text, prob, max_ratio)

            elif attack_type == 'reorder':
                strength_ratio = float(params.get('Strength', 0.3))
                distance = int(params.get('Distance', 5))
                words = text.split()
                strength = int(len(words) * strength_ratio)
                return self.reorder_attack(text, strength, distance)

            elif attack_type == 'syn_transform':
                strength = float(params.get('Strength', 0.3))
                return self.syn_transform_attack(text, strength)

            elif attack_type == 'paraphrase':
                temperature = float(params.get('Temperature', 1))
                return self.paraphrasing_attack(
                    text,
                    temperature=temperature
                )

            elif attack_type == 'translation':
                language = params.get('Language', 'ja')
                return self.translation_attack(text, language)

            else:
                print("Unknown attack type")
                return text

        except Exception as e:
            print(f"Attack failed: {e}")
            return text


