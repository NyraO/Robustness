import difflib
from generate import generate_watermarked_text, evaluate_watermark
from attack import *

# --- HELPER: Visualization ---
def print_highlighted(original_text, modified_text):
    GREEN = '\033[92m' # Unchanged
    RED = '\033[91m'   # Changed/Added
    RESET = '\033[0m'
    
    a = original_text.split()
    b = modified_text.split()
    matcher = difflib.SequenceMatcher(None, a, b)
    
    output = []
    for opcode, a0, a1, b0, b1 in matcher.get_opcodes():
        if opcode == 'equal':
            output.append(GREEN + " ".join(a[a0:a1]) + RESET)
        elif opcode == 'insert':
            output.append(RED + " ".join(b[b0:b1]) + RESET)
        elif opcode == 'replace':
            output.append(RED + " ".join(b[b0:b1]) + RESET)
        elif opcode == 'delete':
            pass # Hide deleted words to keep it readable
            
    print(" ".join(output))
    print(RESET)

# --- HELPER: Scoring ---
def run_and_evaluate(attack_name, attacked_text, original_score):
    print(f"\n--- {attack_name} Analysis ---")
    
    # 1. Visualize
    print("Diff Visualization:")
    print_highlighted(wm_text, attacked_text) 
    
    # 2. Evaluate
    new_score = evaluate_watermark(attacked_text)
    
    print(f"Original Z-Score: {original_score:.2f}")
    print(f"Attacked Z-Score: {new_score:.2f}")
    
    if new_score < 2.0:
        print(f"RESULT: The {attack_name} successfully DESTROYED the watermark.")
    else:
        print(f"RESULT: The watermark SURVIVED the {attack_name}.")



# Generate Watermarked Text
prompt = "The rapid development of artificial intelligence has led to"
wm_text = generate_watermarked_text(prompt, length=150)

print(f"\n[Generated Text]:\n{wm_text}\n")

# Baseline Score
initial_score = evaluate_watermark(wm_text)

# Define a dummy corpus for copy-paste attack
corpus_text = """
Breaking news from the technology sector. Several new startups have announced
major breakthroughs in quantum computing this week. Investors are watching closely
as the market reacts to these developments.
""" * 10 # Repeat to make it long enough

# Run Attacks

# Attack A: Copy-Paste
# We hide the watermark inside the corpus
result_cp = copy_paste_attack(wm_text, corpus_text, dilution_rate=0.5, position=20)
run_and_evaluate("Copy-Paste Attack", result_cp, initial_score)

# Attack B: Insertion
# We insert random words into the watermark
words_list = ["really", "basically", "actually", "process"]
result_ins = insertion_attack(wm_text, ratio=0.2, words=words_list)
run_and_evaluate("Insertion Attack", result_ins, initial_score)

# Attack C: Noise
# We corrupt words (typos, punctuation)
result_noise = insert_noise_attack(wm_text, ratio=0.15)
run_and_evaluate("Noise Attack", result_noise, initial_score)