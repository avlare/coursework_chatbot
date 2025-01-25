import os
from transformers import MBart50TokenizerFast, MBartForConditionalGeneration

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

model_name = "facebook/mbart-large-50-many-to-many-mmt"
tokenizer_translation = MBart50TokenizerFast.from_pretrained(model_name)
model_translation = MBartForConditionalGeneration.from_pretrained(model_name)


def translate_message(message, tokenizer, model, src_lang, tgt_lang):
    tokenizer.src_lang = src_lang
    inputs = tokenizer(
        message,
        return_tensors="pt",
        padding=True,
        truncation=True
    )
    generated_tokens = model.generate(
        **inputs,
        max_length=512,
        num_beams=5,
        forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang]
    )
    return tokenizer.decode(generated_tokens[0], skip_special_tokens=True)


def translate_user_message(message):
    return translate_message(message, tokenizer_translation, model_translation, "uk_UA", "en_XX")


def translate_bot_message(message):
    return translate_message(message, tokenizer_translation, model_translation, "en_XX", "uk_UA")
