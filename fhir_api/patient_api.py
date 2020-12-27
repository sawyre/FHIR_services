import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import requests
from .sql_query_converter import sql_query_by_dict, sql_query_by_id


REQUEST_API = Blueprint('patient_api', __name__)
 # TODO: Вынести в глобальные и заменить на нужные
CREATE_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/his_requests/"
SEARCH_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/his_requests/"

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

    ans = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=patient_dict)
    print(ans.json())
    return patient_dict, 201

@REQUEST_API.route('/patient/<string:_id>', methods=['GET'])
def get_patient_by_id(_id):
    """
    Get a patient request record
    """
    sql_search_query = sql_query_by_id('patient', _id)
    query_dict = {'query': sql_search_query}
    print(query_dict)
    ans = requests.post(SEARCH_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=query_dict)
    
    return query_dict, 201