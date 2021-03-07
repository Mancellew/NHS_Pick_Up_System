from datetime import datetime, timedelta

import requests
from flask import Blueprint, jsonify, request

from common import requests_commons

prescription_endpoints = Blueprint('prescription_endpoints', __name__)


def __calculate_end_date(repetitions: int, days_frequency: int, first_dose: float) -> float:
    total_prescription_days = (repetitions - 1) * days_frequency
    return (datetime.fromtimestamp(first_dose / 1000) + timedelta(days=total_prescription_days)).timestamp() * 1000


@prescription_endpoints.route('/add_prescription', methods=['POST'])
def add_prescription() -> (dict, int):
    data = request.json if request.is_json else request.form
    try:
        requests_commons.get_and_check(f'http://127.0.0.1:5002/get_patient/{data["patient"]["nhs_number"]}').json()
    except ValueError:
        requests_commons.post_and_check('http://127.0.0.1:5002/add_patient', data["patient"]).json()

    # Not using exceptions for this request simplifies our workflow
    # GPs should be on SystemOne and as such, we will expect to have them all registered
    response = requests.get(f'http://127.0.0.1:5002/get_patient_general_practice/{data["patient"]["nhs_number"]}')
    if response.status_code > 399 or response.json()['general_practice'] != data['general_practice']:
        try:
            __add_patient_gp(data["patient"]["nhs_number"], data["general_practice"])
        except ValueError as err:
            return jsonify(msg='Could not register patient under the GP provided', error=str(err)), 400

    try:
        requests_commons.get_and_check(f'http://127.0.0.1:5002/get_medication/{data["medication_name"]}').json()
        data['end_date'] = __calculate_end_date(data['repetitions'], data['days_frequency'], data['first_dose'])
        data['patient_nhs_number'] = data['patient']['nhs_number']
        response = requests_commons.post_and_check('http://127.0.0.1:5002/add_prescription', data)
    except ValueError:
        # Medications need to be mapped by admins to their required blood tests,
        # so unlike patients they can't just be created
        return jsonify(msg='The medication could not be found'), 404
    return response.json(), response.status_code


@prescription_endpoints.route('/get_prescriptions/<string:nhs_number>', methods=['GET'])
def get_prescriptions(nhs_number: str) -> (dict, int):
    response = requests_commons.get_and_check(f'http://127.0.0.1:5002/get_patient_prescriptions/{nhs_number}')
    patient_prescriptions = response.json()
    return jsonify(patient_prescriptions), 200


def __add_patient_gp(nhs_number, gp_id):
    request_body = {
        'nhs_number': nhs_number,
        'gp_id': gp_id,
        'time_from': datetime.now().isoformat()
    }
    requests_commons.post_and_check(f'http://127.0.0.1:5002/add_patient_general_practice', request_body)
