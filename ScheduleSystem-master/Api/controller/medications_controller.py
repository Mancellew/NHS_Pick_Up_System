from flask import Blueprint, jsonify, request

from common import requests_commons

medication_endpoints = Blueprint('medication_endpoints', __name__)


@medication_endpoints.route('/add_medication', methods=['POST'])
def add_medication() -> (dict, int):
    data = request.json if request.is_json else request.form
    try:
        requests_commons.get_and_check(f'http://127.0.0.1:5002/get_medication/{data["medication_name"]}')
        return jsonify(msg='Medication already exists'), 409
    except ValueError:
        response = requests_commons.post_and_check(f'http://127.0.0.1:5002/add_medication', data)
        return response.json(), 201
