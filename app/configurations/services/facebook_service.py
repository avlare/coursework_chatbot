import requests
import time
import csv
from pathlib import Path

from tokens import APP_TOKEN, FACEBOOK_URL
from app.settings import DELIVERED, UNKNOWN_FORMAT, SENT
from app.settings import SUCCESSFUL_ANSWER_CODE, ACCEPTED_CODE, BAD_REQUEST_CODE

from app.configurations.ai_models.translation import translate_user_message, translate_bot_message
from app.configurations.ai_models.text_generation_llama import generate_answer
from app.configurations.services.user_messages_service import UserMessagesService

from app.configurations.ai_models.text_processing import preprocess_text, postprocess_text

RESULTS_CSV_PATH = Path("response_timings.csv")

if not RESULTS_CSV_PATH.exists():
    with open(RESULTS_CSV_PATH, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "user_id",
            "original_message",
            "translated_user_message_time",  # UK→EN
            "generation_time",
            "translated_back_message_time",  # EN→UK
            "total_send_time",
            "sentences_count",
            "original_user_message",
            "generated_message"
        ])


def send_message(send_id, message):
    json_message = {
        'message': {'text': message},
        'recipient': {'id': send_id}
    }

    auth = {'access_token': APP_TOKEN}

    response = requests.post(FACEBOOK_URL, params=auth, json=json_message)
    response.raise_for_status()

    return response.json()


def write_result_in_csv(user_id, translate_user_time, generation_time, translate_back_time, send_time, sentence_count, original_message, generated_message):
    with open(RESULTS_CSV_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            user_id,
            round(translate_user_time, 3),
            round(generation_time, 3),
            round(translate_back_time, 3),
            round(send_time, 3),
            sentence_count,
            original_message,
            generated_message
        ])


class FacebookService:
    def __init__(self):
        self.message_service = UserMessagesService()

    def is_user_message_valid(self, data):
        return 'entry' in data and 'messaging' in data['entry'][0]

    def check_delivered(self, data):
        return 'delivery' in data

    def check_message_text(self, data):
        return 'message' in data and 'text' in data['message']

    def get_messaging_data(self, data):
        messaging_data = data['entry'][0]['messaging'][0]
        return messaging_data

    def get_user_id(self, data):
        return data['sender']['id']

    def get_user_message_text(self, data):
        return data['message']['text']

    def send_bot_answer(self, user_id, data):
        sentences = preprocess_text(data)
        total_translate_back_time = 0
        total_send_time = 0

        for sentence in sentences:
            start_translate = time.time()
            translated_response = translate_bot_message(sentence)
            total_translate_back_time += time.time() - start_translate

            start_send = time.time()
            postprocessed_response = postprocess_text(translated_response)
            send_message(user_id, postprocessed_response)
            total_send_time += time.time() - start_send

        return total_send_time, total_translate_back_time, len(sentences)

    def validate_message(self, data):
        if not self.is_user_message_valid(data):
            return False, UNKNOWN_FORMAT, BAD_REQUEST_CODE

        messaging_data = self.get_messaging_data(data)

        if self.check_delivered(messaging_data):
            return True, DELIVERED, SUCCESSFUL_ANSWER_CODE

        if not self.check_message_text(messaging_data):
            return False, UNKNOWN_FORMAT, BAD_REQUEST_CODE

        return True, messaging_data, ACCEPTED_CODE

    def add_new_user_message(self, user_id, text):
        if not self.message_service.find_user_by_id(user_id):
            self.message_service.create_user(user_id)
        self.message_service.update_messages(
            user_id, {"role": "user", "content": text}
        )
        return None

    def add_bot_response(self, user_id, text):
        self.message_service.update_messages(
            user_id, {"role": "assistant", "content": text}
        )
        return None

    def process_user_message(self, messaging_data):
        user_id = self.get_user_id(messaging_data)
        message_text = self.get_user_message_text(messaging_data)
        print("Повідомлення: ", message_text)

        start_translate = time.time()
        translated_text = translate_user_message(message_text)
        translate_user_time = time.time() - start_translate
        print("Переклад англійською: ", translated_text)

        self.add_new_user_message(user_id, translated_text)

        all_messages = self.message_service.get_all_messages(user_id)
        start_gen = time.time()
        bot_response = generate_answer(all_messages)
        generation_time = time.time() - start_gen
        print("Відповідь бота: ", bot_response)

        self.add_bot_response(user_id, bot_response)

        send_time, translate_back_time, sentence_count = self.send_bot_answer(user_id, bot_response)

        write_result_in_csv(
            user_id,
            translate_user_time,
            generation_time,
            translate_back_time,
            send_time,
            sentence_count,
            message_text,
            bot_response
        )

        return SENT, SUCCESSFUL_ANSWER_CODE

    def process_message(self, data):
        is_valid, result, code = self.validate_message(data)
        if not is_valid:
            return result, code

        if result == DELIVERED:
            return DELIVERED, SUCCESSFUL_ANSWER_CODE

        return self.process_user_message(result)
