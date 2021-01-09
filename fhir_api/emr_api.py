import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import requests
from .sql_query_function import _get_resources_by_dict, _get_resource_by_id


REQUEST_API = Blueprint('emr_api', __name__)
# TODO: Вынести в глобальные и заменить на нужные
CREATE_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/his_requests/"
SEARCH_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/his_requests/"
EMR_BASE = "/emr"

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


def insert_patient_info(fhir_dict, patient_id, patient_name):
    fhir_dict["subject"] = {
        "reference": patient_id,
        "display": patient_name
    }


def construct_allergy(data, patient_id, patient_name):
    allergy_dict = {"resourceType": "AllergyIntolerance", "clinicalStatus": {
        "text": data["AllergyStatus"]
    }, "verificationStatus": {
        "text": data["AllergyVerification"]
    }, "type": data["Type"], "category": [data["AllergyCategories"]], "criticality": data["Criticality"],
                    "onsetDateTime": data["OnsetDateTime"], "lastOccurrence": data["LastOccurrence"], "patient": {
      "reference": patient_id,
      "display": patient_name
    }}
    return allergy_dict


def construct_observation(data):
    observation_dict = {"resourceType": "Observation", "status": data["ObservationStatus"], "code": {
        "text": data["ObservationText"]
    }, "valueQuantity": {
        "value": data["QuantityValue"],
        "unit": data["QuantityUnit"]
    }, "interpretation": [{
        "text": data["Interpretation"]
    }]}
    return observation_dict


def construct_medical_statement(data, obs_id):
    statement_dict = {"resourceType": "MedicationStatement", "status": data["MedicationStatus"],
                      "partOf": [
                          {
                              "reference": obs_id
                          }
                      ],
                      "medicationCodeableConcept": {
                          "text": data["MedicationConcept"]
                      }, "dateAsserted": data["dateAsserted"], "informationSource": {
            "reference": data["PractitionerID"]
        }, "dosage": [
            {
                "text": data["Dosage"],
                "additionalInstruction": [
                    {
                        "text": data["AdditionalInstruction"]
                    }
                ]
            }
        ]}
    return statement_dict

@REQUEST_API.route(EMR_BASE, methods=['POST'])
def create_emr():
    """
    Create a emr for a patient request
    @return: 201:
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json() or len(request.get_json()) != 3:
        abort(400)
    data = request.get_json()
    patient_id = data[0]["PatientID"]
    patient_name = data[0]["PatientName"]

    observation_fhir = construct_observation(data[0])
    insert_patient_info(observation_fhir, patient_id, patient_name)
    observation_entity = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                       json=observation_fhir)
    print(observation_entity.json())

    allergy_fhir = construct_allergy(data[1], patient_id, patient_name)
    allergy_entity = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                       json=allergy_fhir)
    print(allergy_entity.json())

    new_obs_entity_id = observation_entity.content.id # TODO
    statement_fhir = construct_medical_statement(data[2], new_obs_entity_id)
    insert_patient_info(statement_fhir, patient_id, patient_name)
    statement_entity = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'},
                                       json=statement_fhir)
    print(statement_entity.json())
    return [allergy_fhir, observation_fhir, statement_fhir], 201

@REQUEST_API.route('/get_emr', methods=['POST'])
def get_emr_by_id():
    """
    Get an EMR by patient id
    @return: 200:
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json():
        abort(400)
    data = request.get_json()

    response = None
    return response, 200


# update EMR by patient id
# create new allergy
# create new observation
# create new statement