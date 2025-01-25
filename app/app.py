import subprocess

from flask import Flask, request
from tokens import VERIFY_TOKEN, DOMAIN_ID, APP_TOKEN
import requests

app = Flask(__name__)

FACEBOOK_URL = 'https://graph.facebook.com/v21.0/me/messages'

def send_answer(send_id, message):
    payload = {
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

    requests.post(
        FACEBOOK_URL,
        params=auth,
        json=payload
    )

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token", 403

    elif request.method == 'POST':
        try:
            data = request.json
            print(data)
            if 'entry' in data and 'messaging' in data['entry'][0]:
                messaging_data = data['entry'][0]['messaging'][0]
                if 'message' in messaging_data and 'text' in messaging_data['message']:
                    message = messaging_data['message']['text']
                    send_id = messaging_data['sender']['id']
                    print(message)
                    print(send_id)
                    send_answer(send_id, message)
                    return "Message received", 200


                elif 'delivery' in messaging_data:
                    print(f"Message delivery confirmed: {messaging_data['delivery']}")
                    return "Delivery data received", 200

                else:
                    return "Invalid message format", 400
            else:
                return "Invalid data format", 400
        except Exception as e:
            print(f"Error: {e}")
            return "Internal Server Error", 500


if __name__ == '__main__':
    command = f"ngrok http --domain={DOMAIN_ID} 5000"
    process = subprocess.Popen(command, shell=True)
    try:
        app.run(port=5000)
    finally:
        process.terminate()