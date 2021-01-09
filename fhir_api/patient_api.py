import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import requests
from .sql_query_function import _get_resource_by_id, _get_resources_by_dict
import json


REQUEST_API = Blueprint('patient_api', __name__)
 # TODO: Вынести в глобальные и заменить на нужные
CREATE_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/post_resource/"
SEARCH_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/get_resource/"

#CREATE_RESOURCE_SERVER = "http://b6b33d36f69a.ngrok.io/db_manager/post_resource/"
#SEARCH_RESOURCE_SERVER = "http://b6b33d36f69a.ngrok.io/db_manager/db_request/"

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/create_patient', methods=['POST'])
def create_patient():
    """
    Create a patient request record
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    
    patient_dict = {}
    patient_dict["resourceType"] = "Patient"
    patient_dict["identifier"] = [{"value": str(data["policyNumber"])}]

    # Имена могут меняться или фамилии (при женитьбе), поэтому список
    names_list_dict = [{}]
    names_list_dict[0]["use"] = "official"
    names_list_dict[0]["given"] = [data['name']]
    names_list_dict[0]["family"] = data['family']
    patient_dict["name"] = names_list_dict

    patient_dict["gender"] = data['gender']
    # Формат YYYY-MM-DD
    patient_dict["birthDate"] = data['birthDate']
    
    # Список средств связи
    telecom_list_dict = [{}]
    telecom_list_dict[0]["system"] = "phone"
    telecom_list_dict[0]["value"] = data['phoneNumber']
    telecom_list_dict.append({'system': 'email', 'value': data['email']})
    patient_dict["telecom"] = telecom_list_dict

    # Список адресов
    address_list_dict = [{}]
    address_list_dict[0]['line'] = [data['address']]
    address_list_dict[0]['city'] = data['city']
    address_list_dict[0]['state'] = data['state']
    patient_dict['address'] = address_list_dict
    print(patient_dict)
    print(CREATE_RESOURCE_SERVER)
    ans = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=patient_dict)
    print(json.loads(ans.json()["success"][0][0]))
    return json.loads(ans.json()["success"][0][0]), 201

@REQUEST_API.route('/patient/<string:_id>', methods=['GET'])
def get_patient_by_id(_id):
    """
    Get a patient request record
    """
    ans = _get_resource_by_id('patient', _id)
    
    return ans, 201

def _get_patient_by_policyNumber(policyNumber):
    search_dict = {"identifier": [{"value": str(policyNumber)}]}
    patient_dict = _get_resources_by_dict('patient', search_dict)
    return patient_dict

@REQUEST_API.route('/get_patient', methods=['POST'])
def get_patient():
    """
    Get a patient request record
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    patient_dict = _get_patient_by_policyNumber(data["policyNumber"])
    
    return patient_dict, 201