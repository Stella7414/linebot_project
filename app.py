from flask import Flask
from handlers import setup_webhook

app = Flask(__name__)
setup_webhook(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)