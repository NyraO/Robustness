# Robustness


## 📂 Project Structure 

* **`main.py`**  This is the orchestrator. It handles input selection (MarkLLM vs. File Upload), calls the attack functions, and runs the scoring logic. **Run this file to start the analysis.**
* **`attack.py`**
    * Contains the library of attack functions (Copy-Paste, Deletion, Synonym Swap, LLM Paraphrasing). All functions here are **standardized to take a string and return a string.**
* **`generate.py`**
    * **The Generator.** Wraps the `markllm` library to generate watermarked text and calculate Z-scores.
* **`act_pas.py`** (External Dependency)
    * **Grammar Logic.** Helper functions for transforming Active Voice to Passive Voice.
    * speparate github code needed for using syn_transformation function (https://github.com/rishiagarwal2000/Active-to-Passive-Voice)
    * Download the code from: https://github.com/rishiagarwal2000/Active-to-Passive-Voice
    * Make sure the file is named act_pas.py and placed in the root directory.
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

#run the main script. It will execute all of the attacks
python main.py
``` 

### Implemented Attacks
* **`Copy-Paste Attack/`** : Hides the watermarked text inside a larger, unwatermarked corpus.
* **`Insertion/`** : Randomly inserts distinct words into the text.
* **`Insert Noise attack/`** : Adds typos, extra punctuation, and character swaps.
* **`Generative Insertion/`** : Inserts a specific token (e.g., [AI]) at fixed intervals.

* **`Deletion (nth word)/`** : Systematically deletes every n-th word.
* **`Random Deletion/`** : Deletes a specific number of random words.
* **`Portion Deletion/`** : Removes a contiguous block of text.
* **`Reordering/`** : Moves words or sentences to different positions to break N-gram sequences.

* **`Synonym Replacement/`** : Replaces words with their WordNet synonyms while maintaining POS tags.
* **`Active-to-Passive/`** : Grammatically transforms sentences from active voice to passive voice.
* **`LLM Paraphrasing/`** : Uses an external LLM (via Groq) to rewrite the text while preserving meaning.