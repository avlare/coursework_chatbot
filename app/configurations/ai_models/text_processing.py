import re
import nltk

nltk.download("punkt")


def replace_bold_text(text):
    return re.sub(r'\*\*\s*(.*?)\s*\*\*', r'*\1*', text)


def replace_quotes_text(text):
    return re.sub(r'""\s*(.*?)\s*""', r'"\1"', text)


def replace_dots_in_list(text):
    return re.sub(r"(\d+)\.", r"\1@@", text)


def restore_numbered_lists(text):
    return re.sub(r"(\d+)@@", r"\1.", text)


def split_colon(sentence):
    return re.split(r"(:)\s*(\d+\.)", sentence)


def split_sentences(text):
    text = replace_dots_in_list(text)
    sentences = nltk.tokenize.sent_tokenize(text)

    processed_sentences = []
    for sentence in sentences:
        processed_sentences.append(restore_numbered_lists(sentence))

    return processed_sentences


def split_colon_lists(sentences):
    processed = []
    for sentence in sentences:
        parts = split_colon(sentence)
        if len(parts) > 1:
            processed.append(parts[0] + parts[1])
            processed.append(parts[2] + parts[3])
        else:
            processed.append(sentence)
    return processed


def preprocess_text(message):
    sentences = split_sentences(message)
    return split_colon_lists(sentences)


def postprocess_text(sentence):
    sentence = replace_bold_text(sentence)
    sentence = replace_quotes_text(sentence)
    return sentence

