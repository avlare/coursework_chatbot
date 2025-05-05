import pandas as pd
from translation_models import translate_with_timing
from translation_models import helsinki_model_en_uk, helsinki_tokenizer_en_uk
from translation_models import helsinki_model_uk_en, helsinki_tokenizer_uk_en
from translation_models import helsinki_model_fine_tuned, helsinki_tokenizer_fine_tuned
from translation_models import facebook_model, facebook_tokenizer
from statistics_vizualization import plot_translation_times, plot_chrf_distribution
from metrics import statistical_significance_testing
from dir_datasets.datasets_columns import *
from pathes import GOLD_TRANSLATION_DATASET_PATH, TRANSLATION_EN_UKR_PATH


def df_translation_and_time_en_ukr(df):
    df[[helsinki_translation_en_uk, helsinki_time_en_uk]] = df[en].apply(
        lambda text: pd.Series(translate_with_timing(text, helsinki_model_en_uk, helsinki_tokenizer_en_uk))
    )

    df[[facebook_translation_en_uk, facebook_time_en_uk]] = df[en].apply(
        lambda text: pd.Series(translate_with_timing(text, facebook_model, facebook_tokenizer, "en_XX", "uk_UA"))
    )

    df[[helsinki_translation_fine_tuned, helsinki_time_fine_tuned]] = df[en].apply(
        lambda text: pd.Series(translate_with_timing(text, helsinki_model_fine_tuned, helsinki_tokenizer_fine_tuned))
    )

    plot_translation_times(df, helsinki_time_en_uk, facebook_time_en_uk, "Helsinki",
                           "Facebook_en_ukr", "English-Ukrainian")
    plot_translation_times(df, helsinki_time_fine_tuned, facebook_time_en_uk, "Helsinki_Fine_Tuned",
                           "Facebook_en_ukr", "English-Ukrainian")
    return df


def chrf_results_en_ukr(df):
    statistical_significance_testing(df[ukr].astype(str).tolist(),
                                     df[helsinki_translation_en_uk].astype(str).tolist(),
                                     df[facebook_translation_en_uk].astype(str).tolist(),
                                     "Helsinki_eng_ukr", "Facebook_eng_ukr")

    statistical_significance_testing(df[ukr].astype(str).tolist(),
                                     df[helsinki_translation_fine_tuned].astype(str).tolist(),
                                     df[facebook_translation_en_uk].astype(str).tolist(),
                                     "Helsinki_Fine_Tuned", "Facebook_eng_ukr")

    plot_chrf_distribution("chrf_Helsinki_eng_ukr_vs_Facebook_eng_ukr",
                           "English-Ukrainian")
    plot_chrf_distribution("chrf_Helsinki_Fine_Tuned_vs_Facebook_eng_ukr",
                           "English-Ukrainian")
    return


def df_translation_and_time_ukr_en(df):
    df[[helsinki_translation_uk_en, helsinki_time_uk_en]] = df[ukr].apply(
        lambda text: pd.Series(translate_with_timing(text, helsinki_model_uk_en, helsinki_tokenizer_uk_en))
    )

    df[[facebook_translation_uk_en, facebook_time_uk_en]] = df[ukr].apply(
        lambda text: pd.Series(translate_with_timing(text, facebook_model, facebook_tokenizer,
                                                     "uk_UA", "en_XX"))
    )

    plot_translation_times(df, helsinki_time_uk_en, facebook_time_uk_en, "Helsinki_ukr_eng",
                           "Facebook_ukr_eng", "Ukrainian-English")

    return df


def chrf_results_ukr_en(df):
    statistical_significance_testing(df[en].astype(str).tolist(),
                                     df[helsinki_translation_uk_en].astype(str).tolist(),
                                     df[facebook_translation_uk_en].astype(str).tolist(),
                                     "Helsinki_ukr_en", "Facebook_ukr_en")

    plot_chrf_distribution("chrf_Helsinki_ukr_en_vs_Facebook_ukr_en",
                           "Ukrainian-English")
    return
