import os

from flask import Blueprint, jsonify, render_template, request
from flask_mail import Message

from common import yaml_commons
from extensions import mail

notification_endpoints = Blueprint('notification_endpoints', __name__)
current_dir = os.path.dirname(os.path.realpath(__file__))
config = yaml_commons.load_from_file(f'{current_dir}/../config.yml')
sender: str = config['smtp']['email']


@notification_endpoints.route('/notify_pickup', methods=['POST'])
def notify_pickup() -> (dict, int):
    data = request.json if request.is_json else request.form

    mail_html = render_template('pickup_patient.html',
                                patient_fullname=data['patient_name'],
                                medication_name=data['medication'],
                                pickup_date=data['pickup_date'])
    msg = Message('New Upcoming Pickup',
                  sender=sender,
                  recipients=[data['patient_email']])
    msg.html = mail_html
    mail.send(msg)

    # TODO send sms

    return jsonify(msg='Email sent'), 200


@notification_endpoints.route('/notify_blood_test', methods=['POST'])
def notify_blood_test() -> (dict, int):
    data = request.json if request.is_json else request.form

    # notify doctor
    mail_html = render_template('blood_test_doctor.html',
                                doctor_name=data['general_practice_name'],
                                patient_fullname=data['patient_name'],
                                test_name=data['blood_test_type'])
    msg = Message('New Pending Blood Test',
                  sender=sender,
                  recipients=[data['general_practice_email']])
    msg.html = mail_html
    mail.send(msg)

    # notify patient
    mail_html = render_template('blood_test_patient.html',
                                patient_fullname=data['patient_name'],
                                test_name=data['blood_test_type'])
    msg = Message('New Pending Blood Test',
                  sender=sender,
                  recipients=[data['patient_email']])
    msg.html = mail_html
    mail.send(msg)

    return jsonify(msg='Email sent'), 200
