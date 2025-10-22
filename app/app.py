from flask import Flask, render_template, jsonify, Response, request
from flaskwebgui import FlaskUI
import random

app: Flask = Flask(__name__, template_folder="template")

ui: FlaskUI = FlaskUI(app=app, server="flask", width=500, height=500)

push_data = True


@app.route("/")
def index() -> str:
    """
    Returns the generated string of the html from index.html
    """
    return render_template("index.html")


@app.route("/data_route")
def data_route() -> Response:
    """
    Basic data route.
    """
    global push_data
    data = [
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    ]
    return jsonify(data) if push_data else jsonify([])


@app.route("/jumping-data-route")
def jumping_data_route() -> Response:
    """
    a"""
    global push_data
    data = [
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
        {"x": random.randint(0, 100), "y": random.randint(0, 100)},
    ]
    return jsonify(data) if push_data else jsonify([])


@app.route("/recv-output", methods=["POST"])
def recv_output() -> Response:
    """
    a"""
    global push_data
    if request.method == "POST":
        print(request.form)
        data = request.get_json()
        print(data)
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
