from threading import Thread
import time

import requests
from tokens import APP_TOKEN, FACEBOOK_URL

from app.ai_models.translation import translate_user_message, translate_bot_message
from app.ai_models.text_generation_llama import generate_answer
from app.services.user_messages_service import UserMessagesService


class FacebookService:
    def __init__(self):
        self.message_service = UserMessagesService()

    def process_message(self, data):
        print("HEEEEEEEEEEEEEREEEEEE")
        if 'entry' in data and 'messaging' in data['entry'][0]:
            messaging_data = data['entry'][0]['messaging'][0]

            if 'delivery' in messaging_data:
                return "Delivered", 200

            if 'message' in messaging_data and 'text' in messaging_data['message']:
                user_id = messaging_data['sender']['id']
                message_text = messaging_data['message']['text']

                translated_text = translate_user_message(message_text)
                if self.message_service.find_user_by_id(user_id) is None:
                    self.message_service.create_user(user_id)
                self.message_service.update_messages(user_id, {"role": "user", "content": translated_text})

                all_messages = self.message_service.get_all_messages(user_id)

                bot_response = generate_answer(all_messages)

                self.message_service.update_messages(user_id, {"role": "assistant", "content": bot_response})

                translated_response = translate_bot_message(bot_response)
                self.send_answer_async(user_id, translated_response)
                return "Sent message", 200

        return "Unknown data format", 400

    def send_answer_async(self, send_id, message):
        def task():
            try:
                self.send_answer(send_id, message)
            except Exception as e:
                print(e)

        Thread(target=task).start()

    def send_answer(self, send_id, message):
        json_message = {
            'message': {
                'text': message
            },
            'recipient': {
                'id': send_id
            }
        }

        auth = {
            'access_token': APP_TOKEN
        }

        for attempt in range(1):  # Максимум 3 спроби
            response = requests.post(FACEBOOK_URL, params=auth, json=json_message)
            if response.status_code == 200:
                return
            elif response.status_code == 503:
                print(f"Retrying ({attempt + 1}) due to 503 error...")
                time.sleep(2)  # Очікування між спробами
            else:
                print(f"Failed to send message: {response.status_code}")
                break

