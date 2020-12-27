import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import requests


REQUEST_API = Blueprint('schedule_api', __name__)
SERVER = "https://hisgateway.herokuapp.com/panel/his_requests/"

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


@REQUEST_API.route('/schedule', methods=['POST'])
def create_schedule():
    """
    Create a schedule request record
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json():
        abort(400)
    data = request.get_json()

    schedule_dict = {}
    schedule_dict['resourceType'] = "Schedule"

    serviceCat = [{
        "coding": [
            {
                "code": data["serviceCategoryCode"],
                "display": data["serviceCategory"]
            }
        ]
    }]
    schedule_dict["serviceCategory"] = serviceCat

    serviceType = [{
        "coding": [
            {
                "code": data["serviceTypeCode"],
                "display": data["serviceType"]
            }
        ]
    }]
    schedule_dict["serviceType"] = serviceCat

    specialty = [{
        "coding": [
            {
                "code": data["specialtyCode"],
                "display": data["specialty"]
            }
        ]
    }]
    schedule_dict["specialty"] = serviceCat

    actors = [
        {
            "reference": "Practitioner/" + str(data["PractitionerID"]),
            "display": data["Practitioner"]
        },
        {
            "reference": "Location/" + str(data["LocationID"]),
            "display": data["Location"]
        }
    ]
    schedule_dict["actor"] = actors

    schedule_dict["planningHorizon"] = {
        "start": data["StartDate"],
        "end": data["EndDate"]
    }

    return schedule_dict, 201

@REQUEST_API.route('/schedule', methods=['GET'])
def get_schedule():
    """
    Get a schedule request record
    """
    if not request.get_json():
        abort(400)
    data = request.get_json(force=True)
    
    ans = requests.post(SERVER, headers={'Content-type': 'application/json'}, json=data)
    
    return data, 201