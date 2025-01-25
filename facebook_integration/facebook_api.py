import requests
from tokens import APP_TOKEN

FACEBOOK_URL = 'https://graph.facebook.com/v21.0/me/messages'


def get_text(data):
    if 'entry' in data and 'messaging' in data['entry'][0]:
        messaging_data = data['entry'][0]['messaging'][0]
        if 'message' in messaging_data and 'text' in messaging_data['message']:
            message = messaging_data['message']['text']
            send_id = messaging_data['sender']['id']
            send_answer(send_id, message)
            return "Got message", 200
        elif 'delivery' in messaging_data:
            return "Delivered message", 200
    else:
        return "Unknown data format", 400


def send_answer(send_id, message):
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

    response = requests.post(
        FACEBOOK_URL,
        params=auth,
        json=json_message
    )

