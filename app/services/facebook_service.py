import requests
from tokens import APP_TOKEN, FACEBOOK_URL

from app.ai_models.translation import translate_user_message, translate_bot_message
from app.ai_models.text_generation_llama import generate_answer
from app.services.user_messages_service import UserMessagesService


def send_answer(send_id, message):
    json_message = {
        'message': {'text': message},
        'recipient': {'id': send_id}
    }

    auth = {'access_token': APP_TOKEN}

    response = requests.post(FACEBOOK_URL, params=auth, json=json_message)
    response.raise_for_status()

    return response.json()


class FacebookService:
    def __init__(self):
        self.message_service = UserMessagesService()

    def process_message(self, data):
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
                send_answer(user_id, translated_response)
                return "Sent message", 200

        return "Unknown data format", 400
