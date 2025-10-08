from flask import Flask, render_template
from flaskwebgui import FlaskUI

app: Flask = Flask(__name__, template_folder="template")

ui: FlaskUI = FlaskUI(app=app, server="flask", width=500, height=500)


@app.route("/")
def index() -> str:
    """
    Returns the generated string of the html from index.html
    """
    return render_template("index.html")


if __name__ == "__main__":
    # app.run(debug=True)
    ui.run()
