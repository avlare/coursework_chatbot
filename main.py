import subprocess
from flask import Flask
import time
from tokens import DOMAIN_ID
from app.controllers.facebook_controller import webhook_bp

app = Flask(__name__)

app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    command = f"ngrok http --domain={DOMAIN_ID} 5000"
    process = subprocess.Popen(command, shell=True)
    time.sleep(5)
    try:
        app.run(port=5000, threaded=True)
    finally:
        process.terminate()
