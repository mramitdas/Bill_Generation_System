from flask import Flask, render_template, request, make_response, session, jsonify
from datetime import datetime, timedelta
from database import Database
from functools import wraps
import hashlib
import jwt

app = Flask(__name__)
app.config['SECRET_KEY'] = "amit"
cloud = Database(local=True)


def token_required(func):
    # decorator factory which invoks update_wrapper() method and passes decorated function as an argument
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)

    return decorated


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


@app.route('/home')
@token_required
def home():
    return 'JWT is verified. Welcome to your dashboard !  '


if __name__ == "__main__":
    app.run()
