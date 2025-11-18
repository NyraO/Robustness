def generative_attack(text, token, n):
    """
    Insert a specific token every n words

    Parameters:
    - text: input watermarked text
    - token: token to insert (e.g., "!")
    - n: insert the token after every n words (n >= 1)

    Returns: attacked text
    """
    words = text.split()
    output_words = []

    if n < 1:
        raise ValueError("Parameter n must be at least 1")
    elif n > len(words):
        raise ValueError("Parameter n must be less than the number of words")

    for i, word in enumerate(words, start=1):
        output_words.append(word)
        if i % n == 0:
            output_words.append(token)

    return " ".join(output_words)


# if __name__ == "__main__":
#     src = "A small lantern flickered as the wind carried the scent of pine through the quiet campsite."
#     print("Watermarked Text: ", src)
#     print("Attacked Text:", generative_attack(src, token="!", n=3))
