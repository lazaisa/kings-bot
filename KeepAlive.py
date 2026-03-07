from flask import Flask
from threading import Thread
import os

app = Flask('')

@app.route('/')
def home():
    return "King is Alive! 👑"

def run():
    # Render zahteva da aplikacija slusa na portu koji oni dodele
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # Ovo osigurava da se thread gasi kad i glavni proces
    t.start()
