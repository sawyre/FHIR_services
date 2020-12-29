def construct_observation_resource(data):
    observation_dict = {"resourceType": "Observation", "status": data["ObservationStatus"], "code": {
        "text": data["ObservationText"]
    }, "subject": {
        "reference": "Patient/" + str(data["PatientID"])
    }, "valueQuantity": {
        "value": data["QuantityValue"],
        "unit": data["QuantityUnit"]
    }, "interpretation": [{
        "text": data["Interpretation"]
    }]}
    return observation_dict


def construct_diagnose_resource(data):
    diagnose_dict = {"resourceType": "DiagnosticReport", "code": {
        "text": data["VisitReason"]
    }, "subject": {
        "reference": "Patient/" + str(data["PatientID"])
    }, "effectiveDateTime": (data["EffectiveDateTime"],), "performer": ([{
        "reference": "Practitioner/" + str(data["PractitionerID"])
    }],), "conclusion": data["Conclusion"]}
    obs_result = []
    for observation_id in data["ObservationID"]:
        obs_result.append({
            "reference": observation_id
        })
    diagnose_dict["result"] = obs_result
    return diagnose_dict


def construct_medical_statement_resource(data):
    medication_dict = {"resourceType": "MedicationStatement", "status": data["MedicationStatus"],
                      "medicationCodeableConcept": {
                          "text": data["MedicationConcept"]
                      }, "subject": {
            "reference": "Patient/" + str(data["PatientID"])
        }, "dateAsserted": data["dateAsserted"], "informationSource": {
            "reference": "Practitioner/" + str(data["PractitionerID"])
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
    obs_result = []
    for observation_id in data["ObservationID"]:
        obs_result.append({
            "reference": "Observation/" + str(observation_id)
        })
    medication_dict["partOf"] = obs_result
    return medication_dict
