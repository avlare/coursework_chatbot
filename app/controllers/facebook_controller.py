from queue import Queue
from threading import Thread

from flask import Blueprint, request
from app.services.facebook_service import FacebookService
from tokens import VERIFY_TOKEN

webhook_bp = Blueprint('webhook', __name__)

queue_chats = Queue()


def answering():
    while True:
        data = queue_chats.get()
        if data is None:
            break
        try:
            facebook_service = FacebookService()
            facebook_service.process_message(data)
        except Exception as e:
            print({e})
        finally:
            queue_chats.task_done()


Thread(target=answering, daemon=True).start()


@webhook_bp.route('/webhook', methods=['GET', 'POST'])
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
            queue_chats.put(data)
            return "Accepted", 200
        except Exception as e:
            return f"Server Error {e}", 500
