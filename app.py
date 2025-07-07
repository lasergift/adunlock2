from flask import Flask, render_template
import random
import string
import sqlite3

app = Flask(__name__)

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) + "-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

@app.route("/unlock")
def unlock():
    key = generate_key()
    conn = sqlite3.connect("../db/db.sqlite")
    cur = conn.cursor()
    cur.execute("INSERT INTO keys (key, used) VALUES (?, 0)", (key,))
    conn.commit()
    conn.close()
    return render_template("unlock.html", key=key)

if __name__ == "__main__":
    app.run(debug=True)
