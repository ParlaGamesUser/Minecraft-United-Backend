from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app, supports_credentials=True)
socketio = SocketIO(app, cors_allowed_origins="*")

current_name = ""
progress = 0


@app.route("/name")
def get_name():
    global current_name, progress
    current_name = request.args.get("n")

    progress += 2.5
    if progress > 100:
        progress = 100

    socketio.emit("update_name", current_name)
    socketio.emit("update_progress", progress)

    return current_name


@app.route("/update_progress", methods=["GET"])
def update_progress():
    global progress
    increment = int(request.args.get("inc", 1))
    progress += increment
    if progress > 100:
        progress = 100
    socketio.emit("update_progress", progress)
    return str(progress)


@socketio.on("connect")
def handle_connect():
    if current_name:
        socketio.emit("update_name", current_name)
    socketio.emit("update_progress", progress)


if __name__ == "__main__":
    socketio.run(app, debug=True)
