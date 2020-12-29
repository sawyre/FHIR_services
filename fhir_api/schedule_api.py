import uuid
from datetime import datetime, timedelta
from flask import jsonify, abort, request, Blueprint
import requests
from .sql_query_function import _get_resource_by_id, _get_resources_by_dict
import json


REQUEST_API = Blueprint('schedule_api', __name__)
 # TODO: Вынести в глобальные и заменить на нужные
CREATE_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/post_resource/"
SEARCH_RESOURCE_SERVER = "https://hisgateway.herokuapp.com/panel/get_resource/"

CREATE_RESOURCE_SERVER = "http://0cf4d5f1ce90.ngrok.io/db_manager/post_resource/"
SEARCH_RESOURCE_SERVER = "http://0cf4d5f1ce90.ngrok.io/db_manager/db_request/"


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

@REQUEST_API.route('/create_schedule', methods=['POST'])
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
                "code": str(data["serviceCategoryCode"]),
                "display": data["serviceCategory"]
            }
        ]
    }]
    schedule_dict["serviceCategory"] = serviceCat

    serviceType = [{
        "coding": [
            {
                "code": str(data["serviceTypeCode"]),
                "display": data["serviceType"]
            }
        ]
    }]
    schedule_dict["serviceType"] = serviceCat

    specialty = [{
        "coding": [
            {
                "code": str(data["specialtyCode"]),
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
    
    ans = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=schedule_dict)
    print(json.loads(ans.json()["success"][0][0]))
    return schedule_dict, 201

@REQUEST_API.route('/create_slot', methods=['POST'])
def create_slot():
    """
    Create a slot request record
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json():
        abort(400)
    data = request.get_json()

    slot_dict = {}
    slot_dict['resourceType'] = "Slot"

    serviceCat = [{
        "coding": [
            {
                "code": str(data["serviceCategoryCode"]),
                "display": data["serviceCategory"]
            }
        ]
    }]
    slot_dict["serviceCategory"] = serviceCat

    serviceType = [{
        "coding": [
            {
                "code": str(data["serviceTypeCode"]),
                "display": data["serviceType"]
            }
        ]
    }]
    slot_dict["serviceType"] = serviceType

    specialty = [{
        "coding": [
            {
                "code": str(data["specialtyCode"]),
                "display": data["specialty"]
            }
        ]
    }]
    slot_dict["specialty"] = specialty

    appointmentType = [{
        "coding": [
            {
                "code": str(data["appointmentTypeCode"]),
                "display": data["appointmentType"]
            }
        ]
    }]
    slot_dict["appointmentType"] = appointmentType

    slot_dict['schedule'] = {'reference': "Schedule/" + str(data["ScheduleID"])}

    slot_dict["start"] = data["StartDate"]
    slot_dict["end"] = data["EndDate"]
    
    ans = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=slot_dict)
    print(json.loads(ans.json()["success"][0][0]))
    return slot_dict, 201

@REQUEST_API.route('/create_appointment', methods=['POST'])
def create_appointment():
    """
    Create a appointment request record
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json():
        abort(400)
    data = request.get_json()

    slot_dict = _get_resource_by_id("slot", data['slotID'])

    appointment_dict = {}
    appointment_dict['resourceType'] = "Appointment"

    appointment_dict['status'] = "booked"

    appointment_dict["serviceCategory"] = slot_dict["serviceCategory"]
    appointment_dict["serviceType"] = slot_dict["serviceType"]
    appointment_dict["specialty"] = slot_dict["specialty"]
    appointment_dict["appointmentType"] = slot_dict["appointmentType"]

    appointment_dict["start"] = slot_dict["start"]
    appointment_dict["end"] = slot_dict["end"]

    appointment_dict['slot'] = [{"reference": "Slot/" + str(data['slotID'])}]
    appointment_dict['participant'] = [{"actor": {"reference": "Patient/" +  str(data['patientID'])}}]

    #TODO: создать референс на врача, получив из слота поле референса на расписание

    ans = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=appointment_dict)
    print(ans.json())
    return appointment_dict, 201

@REQUEST_API.route('/get_appointments', methods=['POST'])
def get_appointments():
    """
    Appointments request
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json():
        abort(400)
    data = request.get_json()

    search_dict = {"participant": [{"actor": {"reference": "Patient/" + str(data['patientID'])}}]}
    appointments_dict = _get_resources_by_dict("appointment", search_dict)

    #ans = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=slot_dict)
    print(appointments_dict)
    return appointments_dict, 201

@REQUEST_API.route('/get_slots', methods=['POST'])
def get_slots():
    """
    Slots request
    @return: 201: a new_uuid as a flask/response object \
    with application/json mimetype.
    @raise 400: misunderstood request
    """
    print('here')
    if not request.get_json():
        abort(400)
    data = request.get_json()

    search_dict = {"actor": [{"reference": "Practitioner/" + str(data['practitionerID'])}]}    
    schedule_dict = _get_resources_by_dict("schedule", search_dict)
    #TODO: добавить редактирование результатов по времени
    for key in schedule_dict.keys():
        search_dict = {"schedule": {"reference": "Schedule/" + str(key)}}
        slots_dict = _get_resources_by_dict("slot", search_dict)
        #ans = requests.post(CREATE_RESOURCE_SERVER, headers={'Content-type': 'application/json'}, json=slot_dict)
        return slots_dict, 201