import random
import re
from nltk.corpus import wordnet as wn
from nltk import pos_tag


def synonym_attack(text, replace_prob=0.2, max_replace_ratio=0.1, seed=None):
    """
    Paraphrase "watermarked text" randomly substituting words with synonyms

    Parameters
    - text: input watermarked text
    - replace_prob: probability [0..1] to attempt replacing each eligible token
    - max_candidates: maximum number of synonym candidates to consider

    Returns: attacked text
    """

    if seed is not None:
        random.seed(seed)
    tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)  # Tokenize with punctuation preserved
    words_only = [t for t in tokens if t.isalpha()]
    pos_tags = pos_tag(words_only)
    token_word_indices = [i for i, t in enumerate(tokens) if t.isalpha()]
    max_replacements = int(len(words_only) * max_replace_ratio)
    # positions of words to substitute with synonym
    candidate_word_positions = list(range(0, len(words_only), len(words_only) // max_replacements))[:max_replacements]
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


def penn_to_wn_pos(penn_pos: str):
    """Convert Penn Treebank POS tags to WordNet POS tags"""
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


if __name__ == "__main__":
    with open("goethe_text.txt") as file:
        src = str(file.read())
        print("Watermarked Text:", src)
        print("Attacked Text:", synonym_attack(src, replace_prob=0.3, max_replace_ratio=0.8))
