from flask import Blueprint, jsonify, request

from common import requests_commons

patient_general_practice_endpoints = Blueprint('patient_general_practice_endpoints', __name__)


@patient_general_practice_endpoints.route('/get_patient_general_practice/<string:nhs_number>', methods=['GET'])
def get_patient_general_practice(nhs_number: str) -> (dict, int):
    try:
        response = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_patient_general_practice/{nhs_number}')
        return response.json(), 200
    except ValueError as err:
        return jsonify(err), 404
