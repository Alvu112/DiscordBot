from flask import Flask
app = Flask("dummy")

@app.route("/")
def home():
    return "Bot activo!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
