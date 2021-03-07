import os

from flask import Flask

from common import yaml_commons

from extensions import mail


def register_extensions():
    mail.init_app(app)


def register_blueprints():
    from controller.authentication import auth_endpoints
    from controller.system import system_endpoints
    from controller.admins_controller import admin_endpoints
    from controller.blood_test_controller import blood_tests_endpoints
    from controller.medication_blood_tests_controller import medication_blood_tests_endpoints
    from controller.medications_controller import medication_endpoints
    from controller.notifications_controller import notification_endpoints
    from controller.patient_blood_tests_controller import patient_blood_tests_endpoints
    from controller.patient_controller import patient_endpoints
    from controller.patient_general_practice_controller import patient_general_practice_endpoints
    from controller.prescription_controller import prescription_endpoints
    from controller.search_controllers import search_endpoints

    app.register_blueprint(auth_endpoints)
    app.register_blueprint(admin_endpoints)
    app.register_blueprint(blood_tests_endpoints)
    app.register_blueprint(medication_blood_tests_endpoints)
    app.register_blueprint(medication_endpoints)
    app.register_blueprint(notification_endpoints)
    app.register_blueprint(patient_blood_tests_endpoints)
    app.register_blueprint(patient_endpoints)
    app.register_blueprint(patient_general_practice_endpoints)
    app.register_blueprint(prescription_endpoints)
    app.register_blueprint(search_endpoints)
    app.register_blueprint(system_endpoints)


current_dir = os.path.dirname(os.path.realpath(__file__))
config = yaml_commons.load_from_file(f'{current_dir}/config.yml')

app = Flask(__name__, template_folder='./templates')
app.secret_key = config['app_secret_key']

# Config for email server
smtp_config = config['smtp']
app.config['MAIL_SERVER'] = smtp_config['host']
app.config['MAIL_PORT'] = smtp_config['port']
app.config['MAIL_USERNAME'] = smtp_config['email']
app.config['MAIL_PASSWORD'] = smtp_config['password']
app.config['MAIL_USE_TLS'] = str(smtp_config['use_tls']).lower() == 'true'
app.config['MAIL_USE_SSL'] = str(smtp_config['use_ssl']).lower() == 'true'

register_extensions()
register_blueprints()

if __name__ == '__main__':
    app.run()
