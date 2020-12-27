import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import requests


REQUEST_API = Blueprint('patient_api', __name__)
SERVER = "https://hisgateway.herokuapp.com/panel/his_requests/"

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/patient', methods=['POST'])
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
    telecom_list_dict[0]["value"] = data['phone_number']
    patient_dict["telecom"] = telecom_list_dict

    # Список адресов
    address_list_dict = [{}]
    address_list_dict[0]['line'] = [data['address']]
    address_list_dict[0]['city'] = data['city']
    address_list_dict[0]['state'] = data['state']
    patient_dict['address'] = address_list_dict

    ans = requests.post(SERVER, headers={'Content-type': 'application/json'}, json=patient_dict)
    print(ans.json())
    return patient_dict, 201

@REQUEST_API.route('/patient', methods=['GET'])
def get_patient():
    """
    Get a patient request record
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    
    ans = requests.post(SERVER, headers={'Content-type': 'application/json'}, json=data)
    
    return data, 201