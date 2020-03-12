from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

notes = []

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("note") is None:
        session["note"] = []            #多个会话时 可以独立处理
    if request.method == "POST":
        note = request.form.get("note")
        session["note"].append(note)

    return render_template("index.html", notes=session["note"])
