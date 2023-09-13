#!/usr/bin/env python3
"""
Flask application
"""
from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index():
    """Home route"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """Register a user based on email and password form inputs"""
    email, password = request.form.get("email"), request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """Handle login sessions"""
    email, password = request.form.get("email"), request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)
    res = jsonify({"email": email, "message": "logged in"})
    session_id = AUTH.create_session(email)
    res.set_cookie("session_id", session_id)
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
