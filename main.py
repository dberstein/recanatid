from flask import Flask
import random
import string
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "john": generate_password_hash("hello"),
    "susan": generate_password_hash("bye")
}
print(users)
@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

def random_user(N: int):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

@app.route("/users")
@auth.login_required
def get_users():
    users = list()
    for _ in range(1, 10):
        users.append(random_user(5))
    return users

app.run('127.0.0.1', 8080, False)