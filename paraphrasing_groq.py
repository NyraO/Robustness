from groq import Groq


def paraphrasing_groq_attack(text, style, temperature=0.6, top_p=0.6, size=1):
    """
    Paraphrase a sentence using LLM

    Parameters:
    ......

    Returns: attacked text
    """

    key = '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'
    task = f"""
    You are a paraphrasing engine. Rewrite the user's text while preserving meaning
    Style: {style}.
    Rules:
    - Do not shorten meaning
    - Do not add new ideas
    - Produce natural and fluent English
    """

    client = Groq(api_key=key)
    res = ""
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": task},
            {"role": "user", "content": text}
        ],
        temperature=temperature,
        max_tokens=int(sum([1 for c in text if c.isalpha()]) * 0.25 * size),
        top_p=top_p,
        stream=True,
        stop=None
    )
    for chunk in completion:
        res += chunk.choices[0].delta.content or ""
    return res


if __name__ == "__main__":
    with open("goethe_text.txt") as file:
        src = str(file.read())
        print("Watermarked Text:", src)
        print("Attacked Text:", paraphrasing_groq_attack(src, "formal", temperature=0.2, top_p=0.2, size=1))
