from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
DB_FILE = "/data/users.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS users (name TEXT)")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("INSERT INTO users (name) VALUES (?)", (name,))
    with sqlite3.connect(DB_FILE) as conn:
        users = conn.execute("SELECT name FROM users").fetchall()
    return render_template_string("""
        <form method="POST">
            What is your name: <input name="name" />
            <input type="submit" />
        </form>
        <ul>
            {% for user in users %}
              <li>{{ user[0] }}</li>
            {% endfor %}
        </ul>
    """, users=users)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
