# The Robustness Project by students of Bauhaus University Weimar WiSe 2025/26
**Goal:** This project was created to analyze the robustness of digital text watermarks

## Procedure 
For analysis, the texts are subjected to attacks, after which they are checked for the presence of watermarks. The following 10 attacks are used for this purpose: 
- **Copy Paste** - hides the watermarked text inside a larger, unwatermarked corpus
- **Insertion** - words or sentences are randomly added into the text
- **Insert noise** - adds typos, extra punctuation, and character swaps
- **Deletion** - randomly removing words from the text
- **Generative** - insert a specific token so that all changes are invertable
- **Paraphrasing** - paraphrase a sentence using LLM
- **Synonym** - paraphrase text randomly substituting words with synonyms
- **Reorder** - moves words or sentences to different positions to break N-gram sequences
- **Syn transform** - rewrite some of the sentences from the active voice to the passive voice
- **Translation** - translate the text from English into the “bridge” language and then back into English

The textseal watermark (https://github.com/facebookresearch/textseal) is used as the main watermarking library

## Project Structure 

```
Robustness/
├── static/
│   ├── skripts.js        # GUI interactions
│   └── styles.css        # Configuration settings for GUI
├── templates/
│   └── interface.html    # Main HTML
├── texts/                # Texts samples for attacks
├── backend.py            # Creating API endpoints and all computations
├── attacks.py            # Attack Engine
```


## Setup & Installation

### 1. Open CMD and move to the project folder

```bash

cd {YOUR_PATH}\Robustness

```

### 2. Environment Setup

```bash

files\Scripts\activate.bat

```


### 3. Run the backend script. It will start hosting web interface
```bash

python backend.py

```

### 4. Open web page [http://localhost:5001/](http://localhost:5001/)


	
## External dependencies:
- textseal library (https://github.com/facebookresearch/textseal)
- Active-to-Passive-Voice library for Syn transformation attack (https://github.com/rishiagarwal2000/Active-to-Passive-Voice)
- The NLTK library for synonym attack (https://www.nltk.org/)
- Hugging Face API for paraphrasing attack (https://huggingface.co/)
- Flask library for web interface (https://flask.palletsprojects.com/en/stable/)
- as well as other built-in Python and JavaScript libraries