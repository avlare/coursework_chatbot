import requests
from threading import Thread
from tokens import APP_TOKEN
from models.chatbot_pipeline import pipeline

FACEBOOK_URL = 'https://graph.facebook.com/v21.0/me/messages'


def get_text(data):
    print(data)
    if 'entry' in data and 'messaging' in data['entry'][0]:
        messaging_data = data['entry'][0]['messaging'][0]

        if 'delivery' in messaging_data:
            pass

        if 'message' in messaging_data and 'text' in messaging_data['message']:
            message = messaging_data['message']['text']
            send_id = messaging_data['sender']['id']

            send_answer_async(send_id, message)
            return "Got message", 200

    return "Unknown data format", 400


def send_answer_async(send_id, message):
    def task():
        try:
            send_answer(send_id, message)
        except Exception as e:
            print(e)

    Thread(target=task).start()


def send_answer(send_id, message):
    bot_response = pipeline(message)
    json_message = {
        'message': {
            'text': bot_response
        },
        'recipient': {
            'id': send_id
        }
    }

    auth = {
        'access_token': APP_TOKEN
    }

    response = requests.post(
        FACEBOOK_URL,
        params=auth,
        json=json_message
    )
