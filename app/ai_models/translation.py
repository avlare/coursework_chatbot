from transformers import AutoTokenizer, MarianMTModel
import nltk

model_name_ukr_en = "Helsinki-NLP/opus-mt-uk-en"
tokenizer_ukr_en = AutoTokenizer.from_pretrained(model_name_ukr_en)
model_ukr_en = MarianMTModel.from_pretrained(model_name_ukr_en)

model_name_en_ukr = "Helsinki-NLP/opus-mt-en-uk"
tokenizer_en_ukr = AutoTokenizer.from_pretrained(model_name_en_ukr)
model_en_ukr = MarianMTModel.from_pretrained(model_name_en_ukr)


def translate_text(text, model, tokenizer):
    sentences = nltk.tokenize.sent_tokenize(text)
    translated_sentences = []

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=512)
        generated_tokens = model.generate(
            **inputs,
            max_new_tokens=256
        )

        translated_text = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)
        translated_sentences.append(translated_text)

    return " ".join(translated_sentences)


def translate_user_message(message):
    return translate_text(message, model_ukr_en, tokenizer_ukr_en)


def translate_bot_message(message):
    return translate_text(message, model_en_ukr, tokenizer_en_ukr)
