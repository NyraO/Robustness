# Robustness


## 📂 Project Structure 

* **`main.py`**  This is the orchestrator. It handles input selection (MarkLLM vs. File Upload), calls the attack functions, and runs the scoring logic. **Run this file to start the analysis.**
* **`attack.py`**
    * Contains the library of attack functions (Copy-Paste, Deletion, Synonym Swap, LLM Paraphrasing). All functions here are **standardized to take a string and return a string.**
* **`generate.py`**
    * **The Generator.** Wraps the `markllm` library to generate watermarked text and calculate Z-scores.
* **`act_pas.py`** / **`act_pas_lib/`**
    * **Grammar Logic.** Helper functions for transforming Active Voice to Passive Voice.
    * *Note: Logic adapted from [Active-to-Passive-Voice](https://github.com/rishiagarwal2000/Active-to-Passive-Voice).*
* **`config/`**
    * Contains algorithm configurations (e.g., `KGW.json`) required by MarkLLM.

## Setup & Installation


### 1. Environment Setup

```bash
# Create venv
python3 -m venv venv
source venv/bin/activate

# Install Core Dependencies
pip install torch transformers nltk groq markllm numpy

```
### 2. Download NLTK Data

```bash

python3 -c "import nltk; nltk.download('averaged_perceptron_tagger'); nltk.download('averaged_perceptron_tagger_eng'); nltk.download('wordnet'); nltk.download('punkt'); nltk.download('punkt_tab')"

```

### 3. Run the main script. It will execute all of the attacks
```bash

python main.py

```


Changing Inputs (Generation vs. Upload)

To switch between generating text with MarkLLM or testing an ad-hoc watermark, edit the configuration at the top of **main.py**
# main.py

### Set to "GENERATE" to use MarkLLM/KGW
### Set to "UPLOAD" to read from a file and apply ad-hoc watermarking
INPUT_MODE = "GENERATE" 

FILE_PATH = "my_document.txt" # Only used if mode is UPLOAD


### Implemented Attacks
* **`Copy-Paste Attack`** : Hides the watermarked text inside a larger, unwatermarked corpus.
* **`Insertion`** : Randomly inserts distinct words into the text.
* **`Insert Noise attack`** : Adds typos, extra punctuation, and character swaps.
* **`Generative Insertion`** : Inserts a specific token (e.g., [AI]) at fixed intervals.

* **`Deletion (nth word)`** : Systematically deletes every n-th word.
* **`Random Deletion`** : Deletes a specific number of random words.
* **`Portion Deletion`** : Removes a contiguous block of text.
* **`Reordering`** : Moves words or sentences to different positions to break N-gram sequences.

* **`Synonym Replacement`** : Replaces words with their WordNet synonyms while maintaining POS tags.
* **`Active-to-Passive`** : Grammatically transforms sentences from active voice to passive voice.
* **`LLM Paraphrasing`** : Uses an external LLM (via Groq) to rewrite the text while preserving meaning.