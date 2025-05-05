import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathes import TRANSLATION_EN_UKR_PATH, COMPARISON_TIME_DIAGRAM, MODEL_COMPARISON_PATH


def plot_translation_times(df, col_a, col_b, model_a, model_b, translation_type):
    models = [model_a, model_b]

    median_times = [
        np.median(df[col_a]),
        np.median(df[col_b])
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(models, median_times, color=['blue', 'green'])
    plt.xlabel('Translation Model')
    plt.ylabel('Median Translation Time (s)')
    plt.title(f'Comparison of {translation_type} Translation Time for Different Models')
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    for i, v in enumerate(median_times):
        plt.text(i, v + 0.02, f"{v:.3f}s", ha='center', fontsize=10)

    plt.savefig(f'{COMPARISON_TIME_DIAGRAM}{model_a}_{model_b}.png')
    plt.show()


def plot_chrf_distribution(filename_prefix, translation_type):
    summary_txt_path = f'{COMPARISON_TIME_DIAGRAM}{filename_prefix}_summary.txt'

    with open(summary_txt_path, 'r') as f:
        first_line = f.readline().strip()
        match = re.search(r'Comparison:\s*(\S+)\s+vs\s+(\S+)', first_line)
        model_a, model_b = match.groups()

        mean_diff = float(f.readline().split(":")[1].strip())
        lower, upper = map(float, f.readline().split(":")[1].strip()[1:-1].split(","))

    filename_prefix = f"chrf_{model_a}_vs_{model_b}"
    df = pd.read_csv(f'{COMPARISON_TIME_DIAGRAM}{filename_prefix}.csv')
    differences = df['differences']

    plt.figure(figsize=(8, 5))
    plt.hist(differences, bins=30, color='lightsteelblue', alpha=0.7, edgecolor='black')
    plt.axvline(lower, color='red', linestyle='dashed', label=f'Lower Bound: {lower:.3f}')
    plt.axvline(upper, color='green', linestyle='dashed', label=f'Upper Bound: {upper:.3f}')
    plt.axvline(mean_diff, color='blue', linestyle='solid', label=f'Mean: {mean_diff:.3f}')

    plt.xlabel('CHRF Score Difference')
    plt.ylabel('Frequency')
    plt.title(f'CHRF Distribution For {translation_type} Translation: {model_a} vs {model_b}')
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f'{COMPARISON_TIME_DIAGRAM}{filename_prefix}_distribution.png')
    plt.show()
