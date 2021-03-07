from flask import Blueprint

system_endpoints = Blueprint('system_endpoints', __name__)


@system_endpoints.route('/ping', methods=['GET'])
def ping() -> str:
    return "System up."
