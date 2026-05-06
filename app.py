from flask import Flask

app = Flask(__name__)

app.secret_key = "secret-key"


@app.route("/")
def home():
    return "<h1>Employee Scheduling App</h1>"


if __name__ == "__main__":
    app.run(debug=True)