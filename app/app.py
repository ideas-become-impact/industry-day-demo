from flask import Flask, render_template, jsonify, Response, request
from flaskwebgui import FlaskUI
import random
import numpy as np
from heartbeat import get_heartbeat, run
from heartbeat.model import predict
import serial

# import heartbeat.get_heartbeat

app: Flask = Flask(__name__, template_folder="template")

ui: FlaskUI = FlaskUI(app=app, server="flask", width=500, height=500)

push_data = True

com_port = "COM4"

ser = serial.Serial(com_port, 115200, timeout=1)

stand_dataset: dict = get_heartbeat.initialize_data_holding_dict()

exercise_dataset: dict = get_heartbeat.initialize_data_holding_dict()

weights = []
bias = []


@app.route("/")
def index() -> str:
    """
    Returns the generated string of the html from index.html
    """
    return render_template("index.html")


@app.route("/data-route", methods=["POST"])
def data_route() -> Response:
    global push_data, ser
    data = []
    # new_data = [
    #     1,
    #     2,
    #     3,
    #     4,
    #     5,
    #     6,
    #     7,
    #     8,
    #     9,
    #     10,
    # ]  # heartbeat.get_heartbeat.get_heartbeat("COM9")
    new_data = get_heartbeat.get_latest_heartbeat(ser, 20, 0, 0.05)

    times = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
    if request.method == "POST":
        added_time = request.get_json()["elapsed_time"]
        data = [
            {"x": added_time + times[i], "y": new_data[i]} for i in range(len(times))
        ]

    return jsonify(data) if push_data else jsonify([])


@app.route("/arduino-read-data", methods=["GET"])
def arduino_read_data() -> Response:

    new_data = get_heartbeat.get_latest_heartbeat(ser, 20, 0, 0.05)

    return jsonify({"data": new_data})

    # data = [
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    #     {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    # ]
    # return jsonify(data) if push_data else jsonify([])


@app.route("/rest-button", methods=["POST"])
def rest_button() -> Response:
    global ser, stand_dataset

    if request.method == "POST":
        current_state = request.get_json()["collect"]
        if current_state:
            # print("Calling!")
            stand_dataset = run.rest_button_clicked(ser, stand_dataset)
            # print("Returning to javascript!")
            return jsonify({"data": stand_dataset})

    return jsonify([])


@app.route("/exercise-button", methods=["POST"])
def exercise_button() -> Response:
    global ser, exercise_dataset

    if request.method == "POST":
        current_state = request.get_json()["collect"]
        # print(current_state)
        if current_state:
            exercise_dataset = run.exercise_button_clicked(ser, exercise_dataset)
            return jsonify({"data": exercise_dataset})

    return jsonify([])


@app.route("/train", methods=["POST", "GET"])
def train() -> Response:
    global stand_dataset, exercise_dataset, weights, bias

    if request.method == "POST":
        is_available = request.get_json()["is_available"]
        if stand_dataset["state"]["filled"] and exercise_dataset["state"]["filled"]:
            _, weights, bias = run.collect_and_train(
                ser, stand_dataset, exercise_dataset
            )

            return jsonify({"ready": True})

    return jsonify({"ready": False})


@app.route("/jumping-data-route", methods=["POST"])
def jumping_data_route() -> Response:
    """
    a"""
    global push_data, ser
    data = []
    # new_data = [
    #     1,
    #     2,
    #     3,
    #     4,
    #     5,
    #     6,
    #     7,
    #     8,
    #     9,
    #     10,
    # ]
    new_data = get_heartbeat.get_latest_heartbeat(ser, 20, 0, 0.05)
    times = np.linspace(0, 1, len(new_data))
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


@app.route("/test")
def test() -> str:
    """
    Returns the generated string of the html from test.html
    """

    return render_template("test.html")


@app.route("/predict", methods=["POST", "GET"])
def predict_route() -> Response:
    global weights, bias

    if request.method == "POST":
        # [data, data, data]
        data = request.get_json()["data"]
        prediction = predict(data, weights, bias)
        state = 0 if prediction[0, 0] <= 0.5 else 1
        return jsonify({"state": state})

    return jsonify([])


if __name__ == "__main__":
    try:
        app.run(debug=True, use_reloader=False)
    finally:
        ser.close()
    # ui.run()
    # hi
