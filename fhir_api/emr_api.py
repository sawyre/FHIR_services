import json

import requests
from flask import abort, request, Blueprint

from fhir_api.patient_api import _get_patient_by_policyNumber
from fhir_api.sql_query_function import _get_resources_by_dict
from utility.constants import CREATE_RESOURCE_SERVER
from utility.resource_constructor import construct_observation_resource, construct_diagnose_resource, \
    construct_medical_statement_resource

REQUEST_API = Blueprint('emr_api', __name__)

getter_patient_id = lambda data: list(_get_patient_by_policyNumber(data['policyNumber']).keys())[0]


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
    patient_id = getter_patient_id(observations[0])
    created_ids = []
    for observation in observations:
        observation_fhir = construct_observation_resource(observation, patient_id)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                 json=observation_fhir)
        created_id = json.loads(response.json()["success"][0][0])["id"]
        created_ids.append(created_id)
    return json.dumps(created_ids), 201


@REQUEST_API.route("/create_diagnoses", methods=['POST'])
def create_diagnoses():
    """
    Create new diagnoses for a patient
    @return: 201: list of created ids
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    diagnoses = request.get_json()
    patient_id = getter_patient_id(diagnoses[0])
    created_ids = []
    for diagnose in diagnoses:
        diagnose_fhir = construct_diagnose_resource(diagnose, patient_id)
        response = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                 json=diagnose_fhir)
        created_id = json.loads(response.json()["success"][0][0])["id"]
        created_ids.append(created_id)
    return json.dumps(created_ids), 201


@REQUEST_API.route("/create_medications", methods=['POST'])
def create_medications():
    """
    Create new medications for a patient
    @return: 201: list of created ids
    @raise 400: misunderstood request
    """
    if not request.get_json():
        abort(400)
    medications = request.get_json()
    patient_id = getter_patient_id(medications[0])
    created_ids = []
    for medication in medications:
        medication_fhir = construct_medical_statement_resource(medication, patient_id)
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
    patient_id = getter_patient_id(request.get_json(force=True))
    search_dict = {"subject": {"reference": "Patient/" + str(patient_id)}}
    observations_dict = _get_resources_by_dict('observation', search_dict)
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
    patient_id = getter_patient_id(request.get_json(force=True))
    search_dict = {"subject": {"reference": "Patient/" + str(patient_id)}}
    diagnoses_dict = _get_resources_by_dict('diagnosticreport', search_dict)
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
    patient_id = getter_patient_id(request.get_json(force=True))
    search_dict = {"subject": {"reference": "Patient/" + str(patient_id)}}
    medications_dict = _get_resources_by_dict('medicationstatement', search_dict)
    return medications_dict, 200
