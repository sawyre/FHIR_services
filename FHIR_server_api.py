import argparse
import os
from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint
from fhir_api import patient_api
from fhir_api import schedule_api
from flask_ngrok import run_with_ngrok


RUN_WITH_NGROK = False
APP = Flask(__name__)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "FHIR_API"
    }
)
APP.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
### end swagger specific ###

APP.register_blueprint(patient_api.get_blueprint())
APP.register_blueprint(schedule_api.get_blueprint())

if RUN_WITH_NGROK:
    run_with_ngrok(APP)

@APP.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(401)
def handle_401_error(_error):
    """Return a http 401 error to client"""
    return make_response(jsonify({'error': 'Unauthorised'}), 401)


@APP.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify({'error': 'Server error'}), 500)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(
        description="Seans-Python-Flask-REST-Boilerplate")

    PARSER.add_argument('--debug', action='store_true',
                        help="Use flask debug/dev mode with file change reloading")
    ARGS = PARSER.parse_args()

    PORT = 5000

    if not RUN_WITH_NGROK:
        print("Running in debug mode")
        CORS = CORS(APP)
        APP.run(host='0.0.0.0', port=PORT, debug=True)
    else:
        APP.run()