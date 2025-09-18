from flask import Flask
import threading
import time
import requests
import os

app = Flask("dummy")

@app.route("/")
def home():
    return "Bot activo!"

def keep_alive():
    url = "http://127.0.0.1:10000"
    while True:
        try:
            requests.get(url)
        except Exception:
            pass
        time.sleep(45)

threading.Thread(target=keep_alive, daemon=True).start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
