from transformers import MarianTokenizer, MarianMTModel
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

model_name_ukr_en = "Helsinki-NLP/opus-mt-uk-en"
tokenizer_ukr_en = MarianTokenizer.from_pretrained(model_name_ukr_en)
model_ukr_en = MarianMTModel.from_pretrained(model_name_ukr_en)

model_name_en_ukr = "D:\\coursework-chatbot\\fine-tuning\\fine_tuned_helsinki"
tokenizer_en_ukr = MarianTokenizer.from_pretrained(model_name_en_ukr)
model_en_ukr = MarianMTModel.from_pretrained(model_name_en_ukr)


def translate_message(message, model, tokenizer, src_lang=None, tgt_lang=None):
    if isinstance(tokenizer, MBart50TokenizerFast):
        tokenizer.src_lang = src_lang

    inputs = tokenizer(
        message,
        return_tensors="pt",
        padding=True,
        truncation=False
    )

    generate_kwargs = {}
    if isinstance(tokenizer, MBart50TokenizerFast):
        generate_kwargs["forced_bos_token_id"] = tokenizer.lang_code_to_id[tgt_lang]

    generated_tokens = model.generate(**inputs, **generate_kwargs)

    return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)


def translate_user_message(message):
    return translate_message(message, model_ukr_en, tokenizer_ukr_en)


def translate_bot_message(message):
    return translate_message(message, model_en_ukr, tokenizer_en_ukr)

