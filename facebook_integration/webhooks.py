from flask import Blueprint, request
from facebook_integration.facebook_api import get_text
from tokens import VERIFY_TOKEN

webhook_bp = Blueprint('webhook', __name__)


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
            res = get_text(data)
            return res
        except Exception:
            return "Server Error", 500
