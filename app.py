from flask import Flask, request
from tokens import VERIFY_TOKEN
import requests

app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge
        return "Invalid verification token", 403

    elif request.method == 'POST':
        data = request.json
        print("Received data:", data)
        return "Event received", 200


if __name__ == '__main__':
    app.run(port=5000)
