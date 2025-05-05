import time
from transformers import MarianMTModel, MarianTokenizer, MBart50TokenizerFast, MBartForConditionalGeneration

helsinki_name_en_uk = "Helsinki-NLP/opus-mt-en-uk"
helsinki_model_en_uk = MarianMTModel.from_pretrained(helsinki_name_en_uk)
helsinki_tokenizer_en_uk = MarianTokenizer.from_pretrained(helsinki_name_en_uk)

helsinki_name_uk_en = "Helsinki-NLP/opus-mt-uk-en"
helsinki_model_uk_en = MarianMTModel.from_pretrained(helsinki_name_uk_en)
helsinki_tokenizer_uk_en = MarianTokenizer.from_pretrained(helsinki_name_uk_en)

helsinki_name_fine_tuned = "D:\\coursework-chatbot\\fine-tuning\\fine_tuned_helsinki"
helsinki_model_fine_tuned = MarianMTModel.from_pretrained(helsinki_name_fine_tuned)
helsinki_tokenizer_fine_tuned = MarianTokenizer.from_pretrained(helsinki_name_fine_tuned)

facebook_name = "facebook/mbart-large-50-many-to-many-mmt"
facebook_model = MBartForConditionalGeneration.from_pretrained(facebook_name)
facebook_tokenizer = MBart50TokenizerFast.from_pretrained(facebook_name)


def translate(message, model, tokenizer, src_lang=None, tgt_lang=None):
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


def translate_with_timing(text, model, tokenizer, *args):
    start_time = time.time()
    result = translate(text, model, tokenizer, *args)
    translation_time = time.time() - start_time
    return result, translation_time

