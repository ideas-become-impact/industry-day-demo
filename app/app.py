from flask import Flask, render_template, jsonify, Response, request
from flaskwebgui import FlaskUI
import random

# import heartbeat.get_heartbeat

app: Flask = Flask(__name__, template_folder="template")

ui: FlaskUI = FlaskUI(app=app, server="flask", width=500, height=500)

push_data = True


@app.route("/")
def index() -> str:
    """
    Returns the generated string of the html from index.html
    """
    return render_template("index.html")


@app.route("/data-route", methods=["POST"])
def data_route() -> Response:
    global push_data
    data = []
    new_data = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
    ]  # heartbeat.get_heartbeat.get_heartbeat("COM9")
    times = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    if request.method == "POST":
        added_time = request.get_json()["elapsed_time"]
        data = [
            {"x": added_time + times[i], "y": new_data[i]} for i in range(len(times))
        ]

    return jsonify(data) if push_data else jsonify([])

    # data = [
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    # ]
    # return jsonify(data) if push_data else jsonify([])


@app.route("/jumping-data-route", methods=["POST"])
def jumping_data_route() -> Response:
    """
    a"""
    global push_data
    data = []
    new_data = [
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        9,
        10,
    ]  # heartbeat.get_heartbeat.get_heartbeat("COM9")
    times = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    if request.method == "POST":
        added_time = request.get_json()["elapsed_time"]
        data = [
            {"x": added_time + times[i], "y": new_data[i]} for i in range(len(times))
        ]

    return jsonify(data) if push_data else jsonify([])


@app.route("/recv-output", methods=["POST"])
def recv_output() -> Response:
    """
    a"""
    global push_data
    if request.method == "POST":
        data = request.get_json()
        push_data = data["push_data"]

    return jsonify([])


@app.route("/home")
def home() -> str:
    """
    Returns the generated string of the html from index.html
    """

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
    # ui.run()
    # hi
