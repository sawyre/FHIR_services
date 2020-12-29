import json

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
    @return: 201: list of created ids
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    observations = request.get_json()
    created_ids = []
    for observation in observations:
        observation_fhir = construct_observation_resource(observation)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                 json=observation_fhir)
        created_id = json.loads(response.json()["success"][0][0])["id"]
        created_ids.append(created_id)
    return json.dumps(created_ids), 201


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
    created_ids = []
    for diagnose in diagnoses:
        diagnose_fhir = construct_diagnose_resource(diagnose)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                 json=diagnose_fhir)
        created_id = json.loads(response.json()["success"][0][0])["id"]
        created_ids.append(created_id)
    return json.dumps(created_ids), 201


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
    created_ids = []
    for medication in medications:
        medication_fhir = construct_medical_statement_resource(medication)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                 json=medication_fhir)
        created_id = json.loads(response.json()["success"][0][0])["id"]
        created_ids.append(created_id)
    return json.dumps(created_ids), 201


@REQUEST_API.route("/get_observations", methods=['POST'])
def get_observations():
    """
    Create new observations for a patient
    @return: 200:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    search_dict = {"subject": {"reference": "Patient/" + str(data["policyNumber"])}}
    observations_dict = _get_resources_by_dict('observation', search_dict)
    observations_dict = {k: json.loads(v) for k, v in observations_dict.items()}
    return observations_dict, 200


@REQUEST_API.route("/get_diagnoses", methods=['POST'])
def get_diagnoses():
    """
    Create new diagnoses for a patient
    @return: 200:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    search_dict = {"subject": {"reference": "Patient/" + str(data["policyNumber"])}}
    diagnoses_dict = _get_resources_by_dict('diagnosticreport', search_dict)
    diagnoses_dict = {k: json.loads(v) for k, v in diagnoses_dict.items()}
    return diagnoses_dict, 200


@REQUEST_API.route("/get_medications", methods=['POST'])
def get_medications():
    """
    Create new medications for a patient
    @return: 200:
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    search_dict = {"subject": {"reference": "Patient/" + str(data["policyNumber"])}}
    medications_dict = _get_resources_by_dict('medicationstatement', search_dict)
    medications_dict = {k: json.loads(v) for k, v in medications_dict.items()}
    return medications_dict, 200
