import random
import numpy as np
import pandas as pd
from sacrebleu.metrics import CHRF
from pathes import MODEL_COMPARISON_PATH, COMPARISON_TIME_DIAGRAM

chrf = CHRF(word_order=2)


def compute_chrf(reference_texts, hypothesis_texts):
    return chrf.corpus_score(hypothesis_texts, [reference_texts]).score


def get_devtest(data, indices):
    return [data[i] for i in indices]


def compute_chrf_difference(gold_translation, translation_a, translation_b, indices):
    sampled_refs = get_devtest(gold_translation, indices)

    text_a = get_devtest(translation_a, indices)
    text_b = get_devtest(translation_b, indices)

    chrf_A = compute_chrf(sampled_refs, text_a)
    chrf_B = compute_chrf(sampled_refs, text_b)
    return chrf_A - chrf_B


def write_differences_and_results_to_file(differences, mean_diff, lower, upper, model_a, model_b):
    filename_prefix = f"chrf_{model_a}_vs_{model_b}"

    results_df = pd.DataFrame({'differences': differences})
    results_csv_path = f"{COMPARISON_TIME_DIAGRAM}{filename_prefix}.csv"
    results_df.to_csv(results_csv_path, index=False)

    summary_txt_path = f"{COMPARISON_TIME_DIAGRAM}{filename_prefix}_summary.txt"
    with open(summary_txt_path, 'w') as f:
        f.write(f"Comparison: {model_a} vs {model_b}\n")
        f.write(f"Mean Difference: {mean_diff:.6f}\n")
        f.write(f"Confidence Interval: ({lower:.6f}, {upper:.6f})\n")

    return results_csv_path, summary_txt_path


def statistical_significance_testing(gold_translation, translation_a, translation_b, model_a, model_b):
    n = 100  # size of gold dataset
    n_datasets = 100
    deviation = 0.025
    differences = []

    for _ in range(n_datasets):
        indices = random.choices(range(n), k=n)
        differences.append(compute_chrf_difference(gold_translation, translation_a, translation_b, indices))

    lower = np.percentile(differences, 100 * deviation)
    upper = np.percentile(differences, 100 * (1 - deviation))
    mean_diff = np.mean(differences)

    return write_differences_and_results_to_file(differences, mean_diff, lower, upper, model_a, model_b)


