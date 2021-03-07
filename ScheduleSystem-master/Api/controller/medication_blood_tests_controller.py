from flask import Blueprint, jsonify, request

from common import requests_commons

medication_blood_tests_endpoints = Blueprint('medication_blood_tests_endpoints', __name__)


@medication_blood_tests_endpoints.route('/add_medication_blood_test', methods=['POST'])
def add_medication_blood_test() -> (dict, int):
    data = request.json if request.is_json else request.form
    try:
        requests_commons.get_and_check(f'http://127.0.0.1:5002/get_medication_blood_test/{data["medication_name"]}/{data["blood_test_type"]}')
        return jsonify(msg='This blood test is already linked to the medication provided'), 409
    except ValueError:
        response = requests_commons.post_and_check(f'http://127.0.0.1:5002/add_medication_blood_test', data)
        return response.json(), 201


@medication_blood_tests_endpoints.route('/get_medication_blood_test/<string:medication>', methods=['GET'])
def get_patient_blood_tests(medication: str) -> (dict, int):
    medication_blood_tests = requests_commons.get_and_check(
        f'http://127.0.0.1:5002/get_medication_blood_tests/{medication}')
    return jsonify(medication_blood_tests.json()), medication_blood_tests.status_code
