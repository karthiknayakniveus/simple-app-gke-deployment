from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)
DB_FILE = "/data/todo.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT
            )
        """)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        if title:
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute("INSERT INTO todos (title, description) VALUES (?, ?)", (title, description))

    with sqlite3.connect(DB_FILE) as conn:
        todos = conn.execute("SELECT title, description FROM todos").fetchall()

    return render_template_string("""
    <html>
      <head>
        <title>To-Do List</title>
        <style>
          body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 40px auto;
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
          }
          h1 {
            text-align: center;
            color: #333;
          }
          form {
            margin-bottom: 30px;
          }
          input[type="text"], textarea {
            width: 100%;
            padding: 10px;
            margin-top: 8px;
            margin-bottom: 16px;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-sizing: border-box;
          }
          input[type="submit"] {
            background-color: #007bff;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
          }
          input[type="submit"]:hover {
            background-color: #0056b3;
          }
          ul {
            list-style-type: none;
            padding: 0;
          }
          li {
            background: #ffffff;
            border: 1px solid #ddd;
            margin-bottom: 10px;
            padding: 10px;
            border-radius: 5px;
          }
          .title {
            font-weight: bold;
            color: #222;
          }
          .desc {
            color: #555;
          }
        </style>
      </head>
      <body>
        <h1>To-Do List</h1>
        <form method="POST">
          <label>Task Title</label>
          <input name="title" type="text" required />
          <label>Description</label>
          <textarea name="description" rows="3"></textarea>
          <input type="submit" value="Add Task" />
        </form>

        <ul>
          {% for todo in todos %}
            <li>
              <div class="title">{{ todo[0] }}</div>
              <div class="desc">{{ todo[1] }}</div>
            </li>
          {% endfor %}
        </ul>
      </body>
    </html>
    """, todos=todos)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000)
