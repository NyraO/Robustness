import random
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk import pos_tag


def nltk_pos_to_wordnet_pos(nltk_pos):
    """Map NLTK POS tags to WordNet POS tags"""
    if nltk_pos.startswith("J"):
        return wordnet.ADJ
    elif nltk_pos.startswith("V"):
        return wordnet.VERB
    elif nltk_pos.startswith("N"):
        return wordnet.NOUN
    elif nltk_pos.startswith("R"):
        return wordnet.ADV
    else:
        return ''


def get_synonyms(word, wn_pos):
    """Return a list of candidate synonyms for 'word' with given wordnet pos"""
    syns = set()
    for syn in wordnet.synsets(word, pos=wn_pos):
        for lemma in syn.lemmas():
            candidate = lemma.name().replace("_", " ")
            # Avoid the identical form (case-insensitive)
            if candidate.lower() != word.lower():
                syns.add(candidate)
    return list(syns)


def synonym_attack(text, replace_prob=0.3, max_candidates=5):
    """
    Paraphrase "watermarked text" randomly substituting words with synonyms

    Parameters
    - text: input watermarked text
    - replace_prob: probability [0..1] to attempt replacing each eligible token
    - max_candidates: maximum number of synonym candidates to consider

    Returns: attacked text
    """
    if not 0 <= replace_prob <= 1:
        raise ValueError("replace_prob must be between 0 and 1")

    tokens = word_tokenize(text)
    tags = pos_tag(tokens)  # list of (token, pos)

    out_tokens = []
    for (token, tag) in tags:
        # Check all tokens are letters (skip punctuation, numbers, etc.)
        if token.isalpha() and random.uniform(0, 1) < replace_prob:
            wn_pos = nltk_pos_to_wordnet_pos(tag)
            if wn_pos:
                candidates = get_synonyms(token, wn_pos)
                if candidates:
                    # limit candidates and pick one at random
                    if len(candidates) > max_candidates:
                        candidates = random.sample(candidates, max_candidates)
                    replacement = random.choice(candidates)
                    # Match the case of the original word
                    if token.isupper():
                        replacement.upper()
                    elif token.islower():
                        replacement.lower()
                    out_tokens.append(replacement)
                    continue  # done for this token
        out_tokens.append(token)  # keep original token for default

    detokenizer = TreebankWordDetokenizer()
    return detokenizer.detokenize(out_tokens)


# if __name__ == "__main__":
#     src = "A small lantern flickered as the wind carried the scent of pine through the quiet campsite."
#     print("Watermarked Text: ", src)
#     print("Attacked Text:", synonym_attack(src, replace_prob=0.3))
