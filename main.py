import difflib
from generate import generate_watermarked_text, evaluate_watermark
from attack import *

INPUT_MODE = "GENERATE" 
FILE_PATH = "texts/goethe.txt"  # Only used if INPUT_MODE is "UPLOAD"

def apply_ad_hoc_watermark(raw_text):
    """
    Take existing text and inject a watermark signal.
    """
    
    # TODO: Replace this with actual watermarking algorithm 
    watermarked_text = raw_text + " " # dummy code
    return watermarked_text

def evaluate_ad_hoc_watermark(text):
 
    # TODO: Replace with actual detection logic
     
    return 10.0 if " " in text else 0.0


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
def run_and_evaluate(attack_name, attacked_text, original_score, evaluator_func):
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

wm_text = ""
current_evaluator = None

if INPUT_MODE == "UPLOAD":
    if not os.path.exists(FILE_PATH):
        # Create a dummy file if it doesn't exist for testing
        with open(FILE_PATH, "w") as f:
            f.write("This is a dummy document created for testing purposes. It simulates a user uploaded file.")
    
    print(f"\n[Mode]: Reading file '{FILE_PATH}'")
    with open(FILE_PATH, 'r') as f:
        raw_input = f.read()
    
    # Apply Watermark (placeholder function)
    wm_text = apply_ad_hoc_watermark(raw_input)
    current_evaluator = evaluate_ad_hoc_watermark

else:
    # Generation (MarkLLM)
    print("\n[Mode]: Generating Text with MarkLLM")
    prompt = "The rapid development of artificial intelligence has led to"
    wm_text = generate_watermarked_text(prompt, length=150)
    current_evaluator = evaluate_watermark

print(f"\n[Baseline Text]:\n{wm_text}\n")
initial_score = current_evaluator(wm_text)


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
run_and_evaluate("Copy-Paste Attack", result_cp, initial_score, current_evaluator)

# Attack B: Insertion
# We insert random words into the watermark
words_list = ["really", "basically", "actually", "process"]
result_ins = insertion_attack(wm_text, ratio=0.2, words=words_list)
run_and_evaluate("Insertion Attack", result_ins, initial_score, current_evaluator)

# Attack C: Noise
# We corrupt words (typos, punctuation)
result_noise = insert_noise_attack(wm_text, ratio=0.15)
run_and_evaluate("Noise Attack", result_noise, initial_score, current_evaluator)

result_gen = generative_attack(wm_text, token="[AI]", n=5)
run_and_evaluate("Generative Token Insert", result_gen, initial_score, current_evaluator)

result_del = deletion(wm_text, strength=3) 
run_and_evaluate("Deletion Attack (nth word)", result_del, initial_score, current_evaluator)

result_rnd_del = delete_random(wm_text, strength=15)
run_and_evaluate("Random Deletion", result_rnd_del, initial_score, current_evaluator)

result_port_del = delete_portion(wm_text, begin=10, end=30)
run_and_evaluate("Portion Deletion", result_port_del, initial_score, current_evaluator)

result_reorder = reorder(wm_text, strength=5, distance=2)
run_and_evaluate("Systematic Reorder", result_reorder, initial_score, current_evaluator)

result_rnd_reorder = reorder_random(wm_text, strength=10, distance=3)
run_and_evaluate("Random Reorder", result_rnd_reorder, initial_score, current_evaluator)

result_max_dist = reorder_random_max_dist(wm_text, strength=10, max_distance=5)
run_and_evaluate("Reorder Max Dist", result_max_dist, initial_score, current_evaluator)

result_syn = synonym_attack(wm_text, replace_prob=0.3)
run_and_evaluate("Synonym Attack", result_syn, initial_score, current_evaluator)

result_pas = syn_transform(wm_text, strength=2)
run_and_evaluate("Active-to-Passive", result_pas, initial_score, current_evaluator)

result_rnd_pas = rand_syn_transform(wm_text, strength=2)
run_and_evaluate("Random Active-to-Passive", result_rnd_pas, initial_score, current_evaluator)

result_para = paraphrasing_attack(wm_text, style="academic", temperature=0.7)
run_and_evaluate("LLM Paraphrasing", result_para, initial_score, current_evaluator)

