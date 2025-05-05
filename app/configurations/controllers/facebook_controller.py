import logging
from queue import Queue
from threading import Thread
from flask import Blueprint, request
from tokens import VERIFY_TOKEN
from app.settings import ACCEPTED, SERVER_ERROR, TOKEN_ERROR
from app.settings import SUCCESSFUL_ANSWER_CODE, FORBIDDEN_CODE, INTERNAL_SERVER_ERROR_CODE
from app.configurations.services.facebook_service import FacebookService

webhook_bp = Blueprint('webhook', __name__)

queue_chats = Queue()


def answering():
    for data in iter(queue_chats.get, None):
        facebook_service = FacebookService()
        result = facebook_service.process_message(data)
        if result[1] != SUCCESSFUL_ANSWER_CODE:
            logging.error(result)
        queue_chats.task_done()


Thread(target=answering, daemon=True).start()


@webhook_bp.route('/webhook', methods=['GET'])
def webhook_get():
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    if token == VERIFY_TOKEN:
        return challenge, SUCCESSFUL_ANSWER_CODE
    return TOKEN_ERROR, FORBIDDEN_CODE


@webhook_bp.route('/webhook', methods=['POST'])
def webhook_post():
    data = request.json
    if not data:
        return SERVER_ERROR, INTERNAL_SERVER_ERROR_CODE

    queue_chats.put(data)
    return ACCEPTED, SUCCESSFUL_ANSWER_CODE

