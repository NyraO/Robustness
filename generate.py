import torch
from markllm.watermark.auto_watermark import AutoWatermark
from markllm.utils.transformers_config import TransformersConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

# Determine Device (Mac uses "cpu" or "mps", but "cpu" is safest for this library)
DEVICE = "cpu" 

print(f"Loading model: facebook/opt-125m on {DEVICE}...")
tokenizer = AutoTokenizer.from_pretrained("facebook/opt-125m")
model = AutoModelForCausalLM.from_pretrained("facebook/opt-125m").to(DEVICE)

# Wrap the model config AND explicitly set the device
# We explicitly tell MarkLLM: "Use the CPU, do not look for a GPU."
x_config = TransformersConfig(
    model=model, 
    tokenizer=tokenizer,
    device=DEVICE 
)

# Initialize Watermarker
watermarker = AutoWatermark.load(
    "KGW",
    algorithm_config="config/KGW.json", 
    transformers_config=x_config
)

def generate_watermarked_text(prompt, length=200):
    print("Generating watermarked text...")
    watermarked_text = watermarker.generate_watermarked_text(
        prompt=prompt, 
        max_new_tokens=length
    )
    return watermarked_text

def evaluate_watermark(text):
    """
    Returns the Z-Score of the watermark in the text.
    """
    result = watermarker.detect_watermark(text)
    
    return result['score']