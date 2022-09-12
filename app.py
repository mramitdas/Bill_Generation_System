from flask import Flask, render_template, request, make_response
from database import Database
import hashlib
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = "amit"
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


@app.route('/login_user', methods=["POST", "GET"])
def login_user():
    if request.method == "POST":
        data = request.form

        if {'email', 'pass'}.issubset(data.keys()):
            email = data['email']
            password = data['pass']
            user_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

            user_data = cloud.fetch(email)

            # missing user in database
            if user_data is None:
                return make_response("User not found", 404)
            else:
                cloud_hash = user_data['secret']

                if user_hash == cloud_hash:
                    token = jwt.encode(
                        payload={'user': email, 'expiry': str(datetime.utcnow() + timedelta(minutes=10))},
                        key=app.config['SECRET_KEY'])

                    return token

                # incorrect password
                else:
                    return make_response('unable to verify', 400)

        # missing value
        else:
            return make_response('unable to verify', 403)


if __name__ == "__main__":
    app.run()
