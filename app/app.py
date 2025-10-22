from flask import Flask, render_template, jsonify, Response
from flaskwebgui import FlaskUI


app: Flask = Flask(__name__, template_folder="template")

ui: FlaskUI = FlaskUI(app=app, server="flask", width=500, height=500)


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
    return jsonify([1, 2, 3, 4, 5])


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


if __name__ == "__main__":
    app.run(debug=True)
    # ui.run()
