def generative_attack(text, token, n):
    """
    Insert a specific token every n words

    Parameters:
    - text: input watermarked text
    - token: token to insert (e.g., "🙃")
    - n: insert the token after every n words

    Returns: attacked text
    """
    words = text.split()
    output_words = []
    for i in range(len(words)):
        output_words.append(words[i])
        if i % n == 0:
            output_words.append(token)
    return " ".join(output_words)


if __name__ == "__main__":
    with open("goethe_text.txt") as file:
        src = str(file.read())
        print("Watermarked Text:", src)
        print("Attacked Text:", generative_attack(src, token="🙃", n=2))
