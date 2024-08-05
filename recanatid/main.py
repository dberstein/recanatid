import datetime
import os
import argparse

from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    JWTManager,
)
from werkzeug.security import generate_password_hash, check_password_hash

from pydantic.dataclasses import dataclass
from .config import DEFAULT_PORT, ACCESS_TOKEN_EXPIRES
from .db import get_db


@dataclass
class User:
    id: str
    name: str
    email: str


get_db().cursor().execute(
    "CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, name TEXT, email TEXT)"
)

app = Flask(__name__)
auth = HTTPBasicAuth()

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.urandom(15).hex()
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_TOKEN_EXPIRES
app.config["JWT_DECODE_AUDIENCE"] = "standard"
jwt = JWTManager(app)

users = {
    "admin": generate_password_hash("secret"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@app.post("/register")
def register():
    pass


@app.post("/login")
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "admin" or password != "secret":
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)


@app.route("/users")
@jwt_required()
def get_users():
    users = []
    for u in get_db().cursor().execute("SELECT id, name, email FROM users").fetchall():
        users.append({"id": u[0], "name": u[1], "email": u[2]})
    return users


@app.post("/users")
@jwt_required()
def post_users():
    # validate json data ...
    for f in ["id", "name", "email"]:
        if f not in request.json:
            return f"Missing field: {f}", 400

    # insert to database ...
    try:
        get_db().cursor().execute(
            "INSERT INTO users (id, name, email) VALUES(?,?,?)",
            (request.json["id"], request.json["name"], request.json["email"]),
        ).connection.commit()
    except Exception as e:
        return "", 400

    # return inserted data
    return request.json, 201


@app.get("/users/<id>")
@jwt_required()
def get_user(id):
    def _get_user():
        for u in (
            get_db()
            .cursor()
            .execute("SELECT id, name, email FROM users WHERE id=?", (id,))
        ):
            return u

    try:
        u = _get_user()
        return {"id": u[0], "name": u[1], "email": u[2]}
    except:
        return "", 404


@app.put("/users/<id>")
@jwt_required()
def put_user(id):
    data = request.json
    print(data)


@app.delete("/users/<id>")
@jwt_required()
def delete_user(id):
    get_db().cursor().execute("DELETE FROM users WHERE id=?", (id,)).connection.commit()
    return ""


parser = argparse.ArgumentParser(
    prog="recanatid",
    description="Recanati HTTP daemon for REST API",
)

parser.add_argument(
    "port",
    default=DEFAULT_PORT,
    help=f"Listen to port number (default: {DEFAULT_PORT})",
    nargs="?",
    type=int,
)


def start():
    args = parser.parse_args()
    app.run("127.0.0.1", args.port)


if __name__ == "__main__":
    start()
