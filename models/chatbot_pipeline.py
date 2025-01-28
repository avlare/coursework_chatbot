import re

from models.text_generation_llama import generate_answer
from models.translation import translate_user_message, translate_bot_message

simple_greetings = ["hi", "hello", "how are you", "hey", "hi how are you"]


def pipeline(message):
    eng_translation = translate_user_message(message)
    answer = None
    if re.sub(r"[,.'?!]", "", eng_translation.lower()) in simple_greetings:
        answer = "Привіт! Я радий, що ти звернувся до мене. Що тебе турбує? :)"
    print(eng_translation)
    response = generate_answer(eng_translation, answer)
    ukrainian_translation = translate_bot_message(response)
    return ukrainian_translation

