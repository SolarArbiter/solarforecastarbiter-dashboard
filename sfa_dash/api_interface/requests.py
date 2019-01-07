""" An Interface for the api.
Currently very simple get/post methods for static dashboard design.
"""
from flask import current_app as app
import json
import requests


def api_get(path):
    url = app.config['SFA_API_URL'] + path
    r = requests.get(url)
    return json.loads(r.text)


def api_post(path, payload):
    url = app.config['SFA_API_URL'] + path
    r = requests.post(url, payload)
    return r.text
