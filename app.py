from flask import Flask, render_template, request
from database import Database
import hashlib

app = Flask(__name__)
cloud = Database(local=True)


@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('login.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    return render_template('register.html')


@app.route('/register_user', methods=["POST", "GET"])
def register_user():
    if request.method == "POST":
        data = request.form

        name = data['name']
        email = data['email']
        password = data['pass']

        cloud.insertion({"name": name,
                         "_id": email,
                         "secret": hashlib.sha256(password.encode('utf-8')).hexdigest(),
                         "auth": "admin"})

        return render_template('register.html')


if __name__ == "__main__":
    app.run()