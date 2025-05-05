import subprocess
from flask import Flask
from tokens import DOMAIN_ID
from app.configurations.controllers.facebook_controller import webhook_bp

app = Flask(__name__)

app.register_blueprint(webhook_bp)

if __name__ == '__main__':
    command = f"ngrok http --domain={DOMAIN_ID} 5000"
    process = subprocess.Popen(command, shell=True)
    try:
        app.run(port=5000, threaded=True)
    finally:
        process.terminate()
