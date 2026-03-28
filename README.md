# The Robustness Project by students of Bauhaus University Weimar WiSe 2025/26
### This project was created to analyze the robustness of digital text (in English) watermarks
### For analysis, the texts are subjected to attacks, after which they are checked for the presence of watermarks. The following 10 attacks are used for this purpose: 
- Copy Paste - watermarked text is inserted into a larger corpus of unwatermarked text, diluting the watermark’s statistical signal
- Insertion - words or sentences are randomly added into the text to change the generated watermark
- Insert noise - creating typical typos to modify the original text
- Deletion - randomly removing words from the text
- Generative - insert a specific token so that all changes are invertable
- Paraphrasing - paraphrase a sentence using LLM
- Synonym - paraphrase text randomly substituting words with synonyms
- Reorder - shuffle the order of some words
- Syn transform - rewrite some of the sentences from the active voice to the passive voice
- Translation - translate the text from English into the “bridge” language and then back into English

### The textseal watermark (https://github.com/facebookresearch/textseal) is used as an example. The following were also used in the project:
- External library for the Syn transformation attack (https://github.com/rishiagarwal2000/Active-to-Passive-Voice)
- The NLTK library for synonym attack (https://www.nltk.org/)
- as well as other built-in Python and JavaScript libraries