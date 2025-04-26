"""
A list of prescribable items
"""
item_types = [
    {
        "name": "medication",
        "description": "Pharmaceutical drugs for treatment or prevention",
        "code": "410942007",
        "code_system": "SNOMED"
    },
    {
        "name": "chemotherapy",
        "description": "Chemical treatment, often for cancer",
        "code": "367336001", "code_system": "SNOMED"
    },
    {
        "name": "radiotherapy",
        "description": "Radiation-based treatment",
        "code": "108290001",
        "code_system": "SNOMED"
    },
    {
        "name": "therapy",
        "description": "Therapeutic sessions like physical or occupational therapy",
        "code": "229065009", "code_system": "SNOMED"
    },  # General 'therapy'
    {
        "name": "surgery",
        "description": "Surgical procedures or minor operations",
        "code": "387713003",
        "code_system": "SNOMED"
    },
    {
        "name": "immunotherapy",
        "description": "Treatment to stimulate or suppress the immune system",
        "code": "367651003",
        "code_system": "SNOMED"
    },
    {
        "name": "psychotherapy",
        "description": "Mental health therapy",
        "code": "18521000",
        "code_system": "SNOMED"
    },
    {
        "name": "nutritional_support",
        "description": "Dietary plans, supplements or feeding support",
        "code": "225341007",
        "code_system": "SNOMED"
    },
    {
        "name": "rehabilitation",
        "description": "Post-treatment or post-injury recovery programs",
        "code": "225358003",
        "code_system": "SNOMED"},
    {
        "name": "vaccination",
        "description": "Administration of vaccines",
        "code": "33879002",
        "code_system": "SNOMED"
    },
    {
        "name": "dialysis",
        "description": "Blood filtration process for kidney patients",
        "code": "108241001",
        "code_system": "SNOMED"
    },
    {
        "name": "medical_device",
        "description": "Prescribed use of medical equipment",
        "code": None,
        "code_system": None
    },  # Highly varied
    {
        "name": "lab_test",
        "description": "Tests requested to support diagnosis",
        "code": "115732007",
        "code_system": "SNOMED"
    }
]
