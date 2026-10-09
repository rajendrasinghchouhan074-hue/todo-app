import json
from pathlib import Path

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
FILE = Path("todos.json")


def load():
    return json.loads(FILE.read_text()) if FILE.exists() else []


def save(todos):
    FILE.write_text(json.dumps(todos, indent=2))


@app.route("/")
def index():
    return render_template("index.html", todos=load())


@app.route("/add", methods=["POST"])
def add():
    text = request.form.get("text", "").strip()
    if text:
        todos = load()
        todos.append({"text": text, "done": False})
        save(todos)
    return redirect(url_for("index"))


@app.route("/toggle/<int:i>")
def toggle(i):
    todos = load()
    if 0 <= i < len(todos):
        todos[i]["done"] = not todos[i]["done"]
        save(todos)
    return redirect(url_for("index"))


@app.route("/delete/<int:i>")
def delete(i):
    todos = load()
    if 0 <= i < len(todos):
        todos.pop(i)
        save(todos)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)