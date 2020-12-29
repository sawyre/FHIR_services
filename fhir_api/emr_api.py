import requests
from flask import abort, request, Blueprint

from fhir_api.sql_query_function import _get_resources_by_dict
from utility.constants import CREATE_RESOURCE_SERVER
from utility.resource_constructor import construct_observation_resource, construct_diagnose_resource, \
    construct_medical_statement_resource

REQUEST_API = Blueprint('emr_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route("/create_observations", methods=['POST'])
def create_observations():
    """
    Create new observations for a patient
    @return: 201: list of created ids??
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    observations = request.get_json()
    created_ids = []
    responses = []  # TODO: remove it later
    for observation in observations:
        observation_fhir = construct_observation_resource(observation)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                             json=observation_fhir)
        responses.append(response)
        # created_ids.append(response.new_id) TODO
    return created_ids, 201


@REQUEST_API.route("/create_diagnoses", methods=['POST'])
def create_diagnoses():
    """
    Create new diagnoses for a patient
    @return: 201:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    diagnoses = request.get_json()
    responses = [] # TODO: remove it later
    for diagnose in diagnoses:
        diagnose_fhir = construct_diagnose_resource(diagnose)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                 json=diagnose_fhir)
        responses.append(response)
    return responses, 201


@REQUEST_API.route("/create_medications", methods=['POST'])
def create_medications():
    """
    Create new medications for a patient
    @return: 201:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    medications = request.get_json()
    responses = []  # TODO: remove it later
    for medication in medications:
        medication_fhir = construct_medical_statement_resource(medication)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                         json=medication_fhir)
        responses.append(response)
    return responses, 201


@REQUEST_API.route("/create_observations", methods=['POST'])
def get_observations():
    """
    Create new observations for a patient
    @return: 200:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    search_dict = {"identifier": [{"value": str(data["policyNumber"])}]}
    observations_dict = _get_resources_by_dict('observation', search_dict)
    return observations_dict, 200


@REQUEST_API.route("/create_diagnoses", methods=['POST'])
def get_diagnoses():
    """
    Create new diagnoses for a patient
    @return: 200:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    search_dict = {"identifier": [{"value": str(data["policyNumber"])}]}
    diagnoses_dict = _get_resources_by_dict('diagnosticreport', search_dict)
    return diagnoses_dict, 200


@REQUEST_API.route("/create_medications", methods=['POST'])
def get_medications():
    """
    Create new medications for a patient
    @return: 200:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    search_dict = {"identifier": [{"value": str(data["policyNumber"])}]}
    medications_dict = _get_resources_by_dict('medicationstatement', search_dict)
    return medications_dict, 200
