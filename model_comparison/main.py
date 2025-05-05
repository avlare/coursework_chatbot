import pandas as pd
from dir_datasets.datasets_columns import *
from pathes import GOLD_TRANSLATION_DATASET_PATH, TRANSLATION_EN_UKR_PATH, TRANSLATION_UKR_EN_PATH
from statistics_vizualization import plot_translation_times
from df_comparison import df_translation_and_time_en_ukr, chrf_results_en_ukr
from df_comparison import df_translation_and_time_ukr_en, chrf_results_ukr_en


def english_to_ukrainian(df):
    df_translation = df_translation_and_time_en_ukr(df)
    df_translation.to_csv(TRANSLATION_EN_UKR_PATH, sep='\t', index=False)
    # df_sample = pd.read_csv(TRANSLATION_EN_UKR_PATH,
    #                         sep='\t', names=[en, ukr, helsinki_translation_en_uk, helsinki_time_en_uk,
    #                                          facebook_translation_en_uk, facebook_time_en_uk,
    #                                          helsinki_translation_fine_tuned, helsinki_time_fine_tuned])
    chrf_results_en_ukr(df_translation)
    return


def ukrainian_to_english(df):
    df_translation = df_translation_and_time_ukr_en(df)
    df_translation.to_csv(TRANSLATION_UKR_EN_PATH, sep='\t', index=False)
    # df_sample = pd.read_csv(TRANSLATION_UKR_EN_PATH,
    #                         sep='\t', names=[en, ukr, helsinki_translation_uk_en, helsinki_time_uk_en,
    #                                          facebook_translation_uk_en, facebook_time_uk_en])
    chrf_results_ukr_en(df_translation)
    return


if __name__ == '__main__':
    dataframe = pd.read_csv(GOLD_TRANSLATION_DATASET_PATH, sep='\t', names=[en, ukr])
    english_to_ukrainian(dataframe)
    ukrainian_to_english(dataframe)
