from datetime import datetime

from flask import Blueprint, jsonify, request

from common import requests_commons

patient_blood_tests_endpoints = Blueprint('patient_blood_test_endpoints', __name__)


@patient_blood_tests_endpoints.route('/add_patient_blood_test', methods=['POST'])
def add_patient_blood_test() -> (dict, int):
    data = request.json if request.is_json else request.form
    data["date_taken"] = datetime.now().timestamp()
    requests_commons.post_and_check('http://127.0.0.1:5002/add_patient_blood_test', data)
    return jsonify(data), 201


@patient_blood_tests_endpoints.route('/get_patient_blood_tests/<string:nhs_number>', methods=['GET'])
def get_patient_blood_tests(nhs_number: str) -> (dict, int):
    patient_blood_tests = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_patient_blood_tests/{nhs_number}')
    return jsonify(patient_blood_tests.json()), patient_blood_tests.status_code
