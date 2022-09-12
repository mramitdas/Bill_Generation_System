from flask import Flask, render_template

app = Flask(__name__)


@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    return render_template('register.html')


if __name__ == "__main__":
    app.run()