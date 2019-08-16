from flask import Flask
import flask
from flask_socketio import SocketIO, emit
import time
import sys

app = Flask(__name__)
app.secret_key = "BPkWbuRcyLfTp7mcwrLB3NTt"  # from random.org
sio = SocketIO(app)

chess_state = {}


def log(msg):
    print("[INFO] [{}] {}",time.strftime("%m/%d %H:%M:%S"),msg)

def warn(msg):
    print("[WARN] [{}] {}", time.strftime("%m/%d %H:%M:%S"), msg)


def chess_prune_rooms():
    log("pruning rooms")
    DELAY = 60
    for g in list(chess_state.keys()):
        if time.time() - chess_state[g]["last_move_s"] > DELAY:
            del chess_state[g]


def get_uname():
    try:
        return flask.session["username"]
    except KeyError:
        flask.session["username"] = "Anonymous"
        return flask.session["username"]


@app.route("/")
def main():
    log("Hit: main page")
    chess_prune_rooms()
    chess_rooms = list(chess_state.keys())
    new = 1  # The new room's number
    while str(new) in chess_rooms:
        new += 1
    s_chess_rooms = []
    for idx, j in enumerate(chess_rooms):
        if chess_state[j]["black"] and chess_state[j]["white"]:
            s_chess_rooms.append(j)
            del chess_rooms[idx]
        elif not (chess_state[j]["black"] or chess_state[j]["white"]):
            del chess_rooms[idx]
    player = {}
    for k, v in chess_state.items():
        s = ""
        if v["wname"] != "N/A":
            s += v["wname"]
            if v["bname"] != "N/A":
                s += ' vs '
                s += v["bname"]
        elif v["bname"] != "N/A":
            s += v["bname"]
        player[k] = s
    return flask.render_template("home.html", chess_rooms=chess_rooms, s_chess_rooms=s_chess_rooms, new=new, player=player)


@app.route("/login")
def login():
    log("Hit: login")
    return flask.render_template('login.html')


@app.route("/", methods=["POST"])
def login_main():
    log("Hit: login return")
    flask.session["username"] = flask.request.form['name']
    log("User with name: {}".format(flask.session["username"]))
    if flask.session["username"] == "N/A":
        warn("Login as 'N/A' ha. ha. ha.")
    return main()


# CHESS


@app.route("/chess/<room>/")
def chess_html(room):
    log("Hit: chess, room {}".format(room))
    return flask.render_template('chess.html', room=room, name=get_uname())


@app.route("/chess/<room>/<path:path>")
def chess(room, path):
    return flask.send_from_directory("chess", path)


@app.route("/chess/<room>/script.js")
def chess_script(room):
    return flask.render_template("chess.js", room=room, name=get_uname())


@sio.on("chess move")
def chess_move(msg):
    emit("chess move", msg, broadcast=True)
    chess_state[msg["room"]]["board"] = msg["fen"]
    chess_state[msg["room"]]["last_move_s"] = time.time()


@sio.on("chess reclock")
def chess_reclock(room):
    chess_state[room]["last_move_s"] = time.time()


@sio.on("chess get")
def chess_get(data):
    try:
        emit("chess get", chess_state[data["room"]])
    except KeyError:
        chess_state[data["room"]] = {}
        chess_state[data["room"]]["board"] = "new"
        chess_state[data["room"]]["white"] = False
        chess_state[data["room"]]["black"] = False
        chess_state[data["room"]]["bname"] = "N/A"
        chess_state[data["room"]]["wname"] = "N/A"
        chess_state[data["room"]]["last_move_s"] = time.time()
        emit("chess get", chess_state[data["room"]])


@sio.on("chess jblack")
def chess_jblack(data):
    emit("chess jblack")
    emit("chess oblack", data, broadcast=True)
    try:
        chess_state[data["room"]]["black"] = True
        chess_state[data["room"]]["bname"] = data["name"]
        log("{} joined black in room {}".format(data["name"], data["room"]))
    except KeyError as err:
        warn("issue joining black, error: {}".format(err))


@sio.on("chess jwhite")
def chess_jwhite(data):
    emit("chess jwhite")
    emit("chess owhite", data, broadcast=True)
    try:
        chess_state[data["room"]]["white"] = True
        chess_state[data["room"]]["wname"] = data["name"]
        log("{} joined white in room {}".format(data["name"], data["room"]))
    except KeyError as err:
        warn("issue joining white, error: {}".format(err))


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 5000
    log("Server running on {}:{}".format(host, port))
    try:
        sio.run(app, host=host, port=port)
    except InterruptedError:
        log("Server stopped by user")
    except:
        err = sys.exc_info()[0]
        warn("Server stopped! {}".format(err))
    finally:
        log("Exiting...")
