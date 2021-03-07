import requests
from flask import Blueprint, jsonify

search_endpoints = Blueprint('search_endpoints', __name__)


@search_endpoints.route('/search_by_nhs_number/<string:nhs_number>', methods=['GET'])
def search_nhs_num(nhs_number: str) -> (dict, int):
    response = requests.get(f'http://127.0.0.1:5002/filter_patients/nhs_number/{nhs_number}')
    return jsonify(response.json()), response.status_code


@search_endpoints.route('/search_by_full_name/<string:name>', methods=['GET'])
def search_full_name(name: str) -> (dict, int):
    response = requests.get(f'http://127.0.0.1:5002/filter_patients/full_name/{name}')
    return jsonify(response.json()), response.status_code


@search_endpoints.route('/search_by_patient_prescription/<string:medication>', methods=['GET'])
def search_patient_prescription(medication: str) -> (dict, int):
    patients_prescriptions = requests.get(f'http://127.0.0.1:5002/filter_patients/patient_prescriptions/{medication}') \
        .json()
    response = []
    for medication in patients_prescriptions:
        patient = requests.get(f'http://127.0.0.1:5002/get_patient/{medication["patient_nhs_number"]}')
        response.append(patient.json())

    return jsonify(response), 200


@search_endpoints.route('/search_by_email/<string:email>', methods=['GET'])
def search_email(email: str) -> (dict, int):
    response = requests.get(f'http://127.0.0.1:5002/filter_patients/email/{email}')
    return jsonify(response.json()), response.status_code
