"""
A list of possible ways of administering prescriptions
"""
a_routes = [
    {
        "name": "oral",
        "description": "Taken by mouth",
        "code": "26643006",
        "code_system": "SNOMED"
    },
    {
        "name": "injection",
        "description": "Administered via needle (IV, IM, SC)",
        "code": None, "code_system": None
    },  # Broad term
    {
        "name": "intravenous",
        "description": "Injected directly into a vein (IV)",
        "code": "47625008",
        "code_system": "SNOMED"
    },
    {
        "name": "intramuscular",
        "description": "Injected into muscle tissue (IM)",
        "code": "78421000",
        "code_system": "SNOMED"
    },
    {
        "name": "subcutaneous",
        "description": "Injected under the skin (SC)",
        "code": "34206005",
        "code_system": "SNOMED"},
    {
        "name": "topical",
        "description": "Applied on the skin",
        "code": "6064005",
        "code_system": "SNOMED"
    },
    {
        "name": "transdermal",
        "description": "Absorbed through skin (e.g., patch)",
        "code": "54485002",
        "code_system": "SNOMED"
    },
    {
        "name": "inhalation",
        "description": "Breathed into the lungs",
        "code": "32106000",
        "code_system": "SNOMED"
    },
    {
        "name": "rectal",
        "description": "Inserted into the rectum",
        "code": "37161004",
        "code_system": "SNOMED"},
    {
        "name": "vaginal",
        "description": "Inserted into the vagina",
        "code": "16857009",
        "code_system": "SNOMED"
    },
    {
        "name": "sublingual",
        "description": "Placed under the tongue",
        "code": "37839007",
        "code_system": "SNOMED"
    },
    {
        "name": "buccal",
        "description": "Placed between gum and cheek",
        "code": "10547007",
        "code_system": "SNOMED"
    },
    {
        "name": "ophthalmic",
        "description": "Applied in the eyes",
        "code": "54471007",
        "code_system": "SNOMED"
    },
    {
        "name": "otic",
        "description": "Applied in the ears",
        "code": "54470006",
        "code_system": "SNOMED"
    },
    {
        "name": "nasal",
        "description": "Applied inside the nose",
        "code": "37739005",
        "code_system": "SNOMED"
    },
    {
        "name": "dermal_implant",
        "description": "Implanted under the skin for slow release",
        "code": None,
        "code_system": None
    },
    {
        "name": "feeding_tube",
        "description": "Delivered via NG, PEG, or G-tube",
        "code": None,
        "code_system": None
    },
    {
        "name": "infusion",
        "description": "Slow continuous administration, typically IV",
        "code": "41795001",
        "code_system": "SNOMED"
    }
]
