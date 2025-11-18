import requests


def paraphrasing_attack(text, diversity=None):
    """
    Paraphrase a sentence using LLM

    Parameters:
    - sentence: input watermarked text
    - temperature: creativity level (the higher, the more creative output text)

    Returns: attacked text
    """

    key = 'PL8WBKHXDJ8BIRQMZXR1P380HMT04UXK'
    url = 'https://api.sapling.ai/api/v1/paraphrase'

    data = {
        'key': key,
        'text': text,
        "num_results": 1,
        "diversity": diversity
    }

    try:
        resp = requests.post(url, json=data)
        # Successful request or not
        if 200 <= resp.status_code < 300:
            resp_json = resp.json()
            results = resp_json["results"]
            return results[0]["replacement"]
        else:
            print('Error: ', str(resp.status_code), resp.text)
    except Exception as e:
        print('Error: ', e)


# if __name__ == "__main__":
#     src = "A small lantern flickered as the wind carried the scent of pine through the quiet campsite."
#     print("Watermarked Text: ", src)
#     print("Attacked Text:", paraphrasing_attack(src, diversity=0.4))
