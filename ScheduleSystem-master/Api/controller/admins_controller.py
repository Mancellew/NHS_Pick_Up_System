

from flask import Blueprint, request

from common import requests_commons
from common.hash_commons import hash_md5

admin_endpoints = Blueprint('admin_endpoints', __name__)


@admin_endpoints.route('/add_admin', methods=['POST'])
def add_admin() -> (object, int):
    data = request.json if request.is_json else request.form
    data['password'] = hash_md5(data['password'])
    response = requests_commons.post_and_check('http://127.0.0.1:5002/add_admin', data)
    return response.content, response.status_code


@admin_endpoints.route('/get_admin/<string:email>', methods=['GET'])
def get_admin(email: str) -> (object, int):
    response = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_admin/{email}')
    response_json = response.json()
    if response_json:
        return response.json(), 200
    else:
        return None, 403
