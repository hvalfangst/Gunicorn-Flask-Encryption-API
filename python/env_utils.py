import os
from flask import request


def get_body():
    text = request.data.decode("utf-8")
    pod_name = os.environ.get("POD_NAME")
    encryption_key = os.environ.get("ENCRYPTION_KEY")
    return encryption_key, pod_name, text


def get_credentials():
    request_data = request.get_json()
    username = request_data.get("username")
    password = request_data.get("password")
    encryption_key = os.environ.get("ENCRYPTION_KEY")
    return encryption_key, password, username
