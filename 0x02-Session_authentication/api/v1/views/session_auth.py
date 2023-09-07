#!/usr/bin/env python3
"""Session view"""
from models.user import User
from flask import request, jsonify
from api.v1.views import app_views


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def login():
    """Handle login and create session ID"""
    email = request.form.get("email")
    password = request.form.get("password")

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search(attributes={"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

        from api.v1.app import auth

        auth.create_session(user.id)
        return user.to_json()
