#!/usr/bin/env python3
"""
Flask application
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
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


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """Handle logout"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """Retrieve user profile"""
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id=session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """Retrieve user's reset token"""
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """Updates a user's password"""
    email, new_password = request.form.get("email"), request.form.get(
        "new_password"
    )
    reset_token = request.form.get("reset_token")
    try:
        AUTH.update_password(reset_token=reset_token, password=new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
