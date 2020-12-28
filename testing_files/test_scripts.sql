SELECT fhirbase_create(
 '{"resourceType": "Patient", "name": [{"family": "Smith"}]}'::jsonb
);

SELECT fhirbase_create(
 '{
    "resourceType": "Observation",
    "status": "final",
    "code": {
      "text": "Glucose [Moles/volume] in blood"
    },
    "subject": {
      "reference": "Patient/b3faa5b2-1232-4f05-8a49-ff9862ef67e4",
      "display": "My super allergic dumb self"
    },
    "valueQuantity": {
      "value": 6.3,
      "unit": "mmol/l"
    },
    "interpretation": [
      {
        "text": "normal"
      }
    ]
  }'::jsonb
);

SELECT fhirbase_create(
 '{
    "resourceType": "AllergyIntolerance",
    "clinicalStatus": {
      "text": "active"
    },
    "verificationStatus": {
      "text": "confirmed"
    },
    "type": "allergy",
    "category": [
      "food",
      "environment",
      "biologic"
    ],
    "criticality": "high",
    "onsetDateTime": "1997",
    "lastOccurrence": "2020",
    "patient": {
      "reference": "Patient/b3faa5b2-1232-4f05-8a49-ff9862ef67e4",
      "display": "My super allergic dumb self"
    }
  }'::jsonb
);

SELECT fhirbase_create(
 '{
    "resourceType": "MedicationStatement",
    "partOf": [
      {
        "reference": "Observation/52660178-0328-4abc-a61e-f2983d830dbf"
      }
    ],
    "status": "active",
    "medicationCodeableConcept": {
      "text": "some antihistamine pill name"
    },
    "subject": {
      "reference": "Patient/b3faa5b2-1232-4f05-8a49-ff9862ef67e4",
      "display": "My super allergic dumb self"
    },
    "dateAsserted": "2020-04",
    "informationSource": {
      "reference": "Practitioner/1222"
    },
    "dosage": [
      {
        "text": "3 times a day",
        "additionalInstruction": [
          {
            "text": "with meals"
          }
        ]
      }
    ]
  }'::jsonb
);

