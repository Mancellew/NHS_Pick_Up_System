from flask import Blueprint, jsonify, request

from common import requests_commons
from common.hash_commons import hash_md5

auth_endpoints = Blueprint('auth_endpoints', __name__)


@auth_endpoints.route('/login', methods=['POST'])
def login() -> (dict, int):
    data = request.json if request.is_json else request.form
    user_type = data['user_type']
    if user_type == 'admin':
        response = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_admin/{data["email"]}').json()
        if response['password'] == hash_md5(data['password']):
            return response, 200
        else:
            return "Incorrect email or password.", 401
    elif user_type == 'nhs_staff':
        if "email" in data:
            response = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_staff/by_email/{data["email"]}')
        else:
            response = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_staff/by_nsh_number/{data["nhs_number"]}')

        json_response = response.json()
        if json_response['password'] == hash_md5(data['password']):
            return json_response, 200
        else:
            return jsonify(msg="Incorrect email or password."), 401
    else:
        return jsonify(msg="User type not recognised"), 401


@auth_endpoints.route('/get_staff/<string:nhs_number>', methods=['GET'])
def get_staff_by_nhs_number(nhs_number: str) -> (dict, int):
    response = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_staff/by_nsh_number/{nhs_number}')
    return response.json(), 200
