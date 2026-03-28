#!/usr/bin/env python3
"""
=============================================================================
ROBUST WATERMARKING SYSTEM
=============================================================================
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import time
from typing import Dict, Tuple
import difflib
import re
import json

from collections import Counter
import math
from huggingface_hub import login
from textseal import PostHocWatermarker, WatermarkConfig, ModelConfig, ProcessingConfig,EvaluationConfig
# Import from the new attack module
from attacks import AttackEngine
import torch
import numpy as np
flag_End_Analyze=False

login(token='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')
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
count = 0
watermarker = 0
WATERMARK_TYPE = "gumbelmax"  # Options: "gumbelmax", "greenlist", "synthid", etc.
MODEL_NAME = "meta-llama/Llama-3.2-1B-Instruct"
TEMPERATURE = 0.9  # https://github.com/facebookresearch/textseal/blob/main/docs/README_posthoc.md
SECRET_KEY = 42
# Force torch to use a specific device string


app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize Attack Engine
attack_engine = AttackEngine()


# =============================================================================
# WATERMARKING FUNCTIONS
# =============================================================================
def create_watermarker(flag=False):
    global watermarker
    watermarker = PostHocWatermarker(
        watermark_config=WatermarkConfig(
            watermark_type=WATERMARK_TYPE,
            secret_key=SECRET_KEY,
        ),
        model_config=ModelConfig(
            model_name=MODEL_NAME,
        ),
        processing_config=ProcessingConfig(temperature=TEMPERATURE),
        evaluation_config=EvaluationConfig(
            enable_detection_only=flag,),
        verbose=False,
    )


def create_watermark_textseal(text: str) -> Dict:
    """Create robust watermark"""
    global watermarker
    global device
    create_watermarker()
    with torch.autocast(device_type=device.type):
        result = watermarker.process_text(text)
    return result


def detect_watermark_robust(text: str, p_value_threshold: float = 0.01) -> Tuple[bool, Dict]:
    """Robust watermark detection"""
    # TOKEN_HUGGING- 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
    global flag_End_Analyze
    global watermarker
    global device
    global count
    if watermarker == 0 or flag_End_Analyze:
        create_watermarker(flag=True)
        flag_End_Analyze=False
        count = 0
    else:
        count += 1

    with torch.autocast(device_type=device.type):
        result = watermarker.evaluate_watermark(text)

    if result["p_value"] <= p_value_threshold:
        result["det"] = True
    else:
        result["det"] = False

    return result["det"], {
        'p-value': round(result["p_value"], 3),
        'threshold': p_value_threshold
    }


def analyze_attack(original: str, modified: str) -> Dict:
    """Analyze what kind of attack was performed"""
    orig_words = original.lower().split()
    mod_words = modified.lower().split()

    matcher = difflib.SequenceMatcher(None, orig_words, mod_words)

    deletions = 0
    insertions = 0
    substitutions = 0
    unchanged = 0

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'delete':
            deletions += (i2 - i1)
        elif tag == 'insert':
            insertions += (j2 - j1)
        elif tag == 'replace':
            substitutions += max(i2 - i1, j2 - j1)
        elif tag == 'equal':
            unchanged += (i2 - i1)

    total_words = len(orig_words)

    deletion_rate = (deletions / total_words * 100) if total_words > 0 else 0
    insertion_rate = (insertions / total_words * 100) if total_words > 0 else 0
    substitution_rate = (substitutions / total_words * 100) if total_words > 0 else 0
    preservation_rate = (unchanged / total_words * 100) if total_words > 0 else 0

    attack_types = []
    if deletion_rate > 5:
        attack_types.append('deletion')
    if insertion_rate > 5:
        attack_types.append('insertion')
    if substitution_rate > 5:
        attack_types.append('paraphrase/substitution')

    if not attack_types:
        attack_types.append('minimal or none')

    return {
        'deletions': deletions,
        'insertions': insertions,
        'substitutions': substitutions,
        'unchanged': unchanged,
        'deletion_rate': round(deletion_rate, 2),
        'insertion_rate': round(insertion_rate, 2),
        'substitution_rate': round(substitution_rate, 2),
        'preservation_rate': round(preservation_rate, 2),
        'attack_types': attack_types,
        'severity': 'high' if max(deletion_rate, insertion_rate, substitution_rate) > 30 else 'medium' if max(
            deletion_rate, insertion_rate, substitution_rate) > 10 else 'low'
    }


# =============================================================================
# Metrics for Analysis computation
# =============================================================================
def compute_confusion(y_true, y_pred):
    tp = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 1)
    fp = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 1)
    tn = sum(1 for t, p in zip(y_true, y_pred) if t == 0 and p == 0)
    fn = sum(1 for t, p in zip(y_true, y_pred) if t == 1 and p == 0)
    return tp, fp, tn, fn


def compute_metrics(y_true, y_pred):
    tp, fp, tn, fn = compute_confusion(y_true, y_pred)

    tpr = tp / (tp + fn) if (tp + fn) > 0 else 0
    fpr = fp / (fp + tn) if (fp + tn) > 0 else 0

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tpr

    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "TPR": tpr,
        "FPR": fpr,
        "F1": f1,
        "total": len(y_true),
        "detected_total": sum(y_pred)
    }


# =============================================================================
# Helper Functions
# =============================================================================

def convert_param_name(name):
    return name.replace("_", " ").title()


def create_params(attack_type):
    params = {}
    grid = [0, 0.2, 0.4, 0.6, 0.8, 1]

    names = {'copy_paste': [" dilution_rate", "position"], 'insert': ["coefficient"],
             'insert_noise': ['coefficient'], 'delete': ['coefficient'], 'generative': ['token_frequency'],
             'synonym': ['max_replace_ratio', 'replace_prob'], 'reorder': ['strength', 'distance'],
             'syn_transform': ['strength'], 'paraphrase': ['temperature'], 'translation': ['language']}

    for na in names[attack_type]:
        if na in ['replace_prob']:
            na = "Replace Probability"
        if na in ['token_frequency', 'distance']:
            params[convert_param_name(na)] = [1, 2, 4, 6, 8, 10]  # possibly a better way?
        elif na in ["max_replace_ratio", "dilution_rate", 'temperature']:
            params[convert_param_name(na)] = [0.01, 0.2, 0.4, 0.6, 0.8, 1]
        elif attack_type == "delete":
            params[convert_param_name(na)] = [0, 0.2, 0.4, 0.6, 0.8, 0.99]
        elif na == 'language':
            params[convert_param_name(na)] = ['es', 'fr', 'de', 'it', 'pt', 'zh-CN', 'ja', 'ko', 'ru', 'ar']
        else:
            params[convert_param_name(na)] = grid
    return params


# =============================================================================
# API ENDPOINTS
# =============================================================================
@app.route('/')
def index():
    return render_template('interface.html')


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'system': 'robust_watermarking'
    })


@app.route('/api/watermark/create', methods=['POST'])
def create_watermark():
    """Create robust watermark"""
    start = time.time()
    try:
        data = request.json
        text = data.get('text', '')

        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        result = create_watermark_textseal(text)
        end = time.time() - start
        result["wm_eval"]["p_value"] = round(result["wm_eval"]["p_value"], 3)
        result["quality"]["semantic_similarity"] = round(result["quality"]["semantic_similarity"] * 100, 3)
        return jsonify({
            'success': True,
            'original_text': text,
            'seconds_exec': round(end, 3),
            'watermarked_text': result["wm_text"],
            'all_returned': result,
            'message': 'Robust watermark created with LLM-based attack testing!',
            'stats': {
                'text_original_length': result["stats"]["orig_len"],
                'text_wm_length': result["stats"]["wm_len"],
                'evaluation_metrics': result["wm_eval"],
                'attack_resistance': 'high'
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/watermark/detect', methods=['POST'])
def detect_watermark():
    """Detect watermark with statistical analysis"""
    try:
        data = request.json
        text = data.get('text', '')
        threshold = data.get('threshold', 0.01)

        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400

        is_detected, details = detect_watermark_robust(text, threshold)

        return jsonify({
            'success': True,
            'is_watermarked': is_detected,
            'details': details
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/watermark/test-attack', methods=['POST'])
def test_attack():
    """Test watermark against attacks"""
    try:
        data = request.json
        original_text = data.get('text', '')
        attack_type = data.get('attack_type', 'paraphrase')

        threshold = data.get('threshold', 0.01)

        if not original_text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400

        parameters = data.get('parameters', {})
        attacked_text = attack_engine.apply_attack(original_text, attack_type, parameters)

        is_detected, details = detect_watermark_robust(attacked_text, threshold)
        attack_analysis = analyze_attack(original_text, attacked_text)

        return jsonify({
            'success': True,
            'original_text': original_text,
            'attacked_text': attacked_text,
            'attack_type': attack_type,
            'parameters': parameters,
            'is_detected': is_detected,
            'detection_details': details,
            'attack_analysis': attack_analysis,
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/watermark/analyze-robustness', methods=['POST'])
def analyze_robustness():
   
    try:
        start = time.time()
        data = request.json
        watermarked_text = data.get("watermarked_text", "")

        clean_text = data.get("clean_text", "")
        threshold = 0.01

        if not watermarked_text or not clean_text:
            return jsonify({"success": False, "error": "No text provided"}), 400

        attack_types = [
            "copy_paste",
            "insert",
            "insert_noise",
            "delete",
            "generative",
            "synonym",
            "reorder",
            "syn_transform",
            "paraphrase",
            "translation"
        ]
        attack_types=attack_types[:7]
        results = {}

        for attack in attack_types:
            parameters = create_params(attack)
            params = {}
            y_true = []
            y_pred = []
            p_values_watermarked = []
            p_values_clean = []

            for p1 in list(parameters.values())[0]:
                params[list(parameters.keys())[0]] = p1
                if len(list(parameters.keys())) != 1:
                    parameters_2 = list(parameters.values())[1]
                else:
                    parameters_2 = [None]
                for p2 in parameters_2:
                    if p2 is not None:
                        params[list(parameters.keys())[1]] = p2

                    attacked_watermarked = attack_engine.apply_attack(
                        watermarked_text,
                        attack,
                        params
                    )
                    detected_watermarked, details = detect_watermark_robust(attacked_watermarked, threshold)
                    
                    p_values_watermarked.append(details.get("p-value", 1))
                    y_true.append(1)
                    y_pred.append(detected_watermarked)

                    attacked_clean = attack_engine.apply_attack(
                        clean_text,
                        attack,
                        params
                    )
                    detected_clean, details_clean = detect_watermark_robust(attacked_clean, threshold)

                    p_values_clean.append(details_clean.get("p-value", 1))
                    y_true.append(0)
                    y_pred.append(detected_clean)

            metrics = compute_metrics(y_true, y_pred)
            results[attack] = {
                "P_value_watermarked": p_values_watermarked,
                "P_value_clean": p_values_clean,
                "params": parameters,
                "metrics": metrics
            }
        # print("Wrote results to log")
        # with open("p-values.json", "w") as file:
        #     json.dump(results,file)
        global flag_End_Analyze
        flag_End_Analyze=True
        
        end_time=time.time()-start
        return jsonify({
            "success": True,
            "results": results,
            "analysis_time_sec": end_time 
        })

    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.errorhandler(Exception)
def handle_exception(err):
    path = request.path  # this var was shown to be 'favicon.ico' or 'manifest.json'
    print(path)
    return jsonify(error=str(err))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    print("=" * 80)
    print("ROBUST WATERMARKING SYSTEM")
    print("=" * 80)
    print("\nStarting Flask server...")
    print("API will be available at: http://localhost:5001")
    print("=" * 80)

    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)
