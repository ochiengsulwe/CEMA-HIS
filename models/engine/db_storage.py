"""Implements the DBStorage.

    The class exposes the following methods:
        `all`, `new`,   `save`, `delete` `reload`, `update`, `close`, `get`, `count`
"""
from api.v1 import db

from models.adult_profile import AdultProfile
from models.appointment import Appointment
from models.child_profile import ChildProfile
from models.date import Date
from models.diagnosis import Diagnosis
from models.diagnostics.category import DiagnosticCategory
from models.diagnostics.link import TestOrderTestLink
from models.diagnostics.order import TestOrder
from models.diagnostics.test import DiagnosticTest
from models.doctors_note import DoctorNote
from models.h_prog import HealthProgram
from models.loginfo import LogInfo
from models.planner import Planner
from models.prac_program import PractitionerProgram
from models.practitioner_profile import PracProfile
from models.prescription.frequency import Frequency
from models.prescription.patient_prescription import PatientPrescription
from models.prescription.prescription_entry import PrescriptionEntry
from models.prescription.typ.chemotherapy.chemo_types.breast import BreastCancer
from models.prescription.typ.chemotherapy.chemo_types.colorectal import (
    ColorectalCancer)
from models.prescription.typ.chemotherapy.chemo_types.leukemia import Leukemia
from models.prescription.typ.chemotherapy.chemo_types.lung import LungCancer
from models.prescription.typ.chemotherapy.chemo_types.lymphoma import Lymphoma
from models.prescription.typ.medication.route import AdministrationRoute
from models.prescription.typ.medication.routes.buccal import Buccal
from models.prescription.typ.medication.routes.dermal_implant import (
    DermalImplant)
from models.prescription.typ.medication.routes.feeding_tube import (
    FeedingTube)
from models.prescription.typ.medication.routes.infusion import Infusion
from models.prescription.typ.medication.routes.inhalation import Inhalation
from models.prescription.typ.medication.routes.injection import Injection
from models.prescription.typ.medication.routes.intramuscular import Intramuscular
from models.prescription.typ.medication.routes.intravenous import Intravenous
from models.prescription.typ.medication.routes.nasal import Nasal
from models.prescription.typ.medication.routes.ophthalmic import Ophthalmic
from models.prescription.typ.medication.routes.oral import Oral
from models.prescription.typ.medication.routes.otic import Otic
from models.prescription.typ.medication.routes.rectal import Rectal
from models.prescription.typ.medication.routes.subcutaneous import Subcutaneous
from models.prescription.typ.medication.routes.sublingual import Sublingual
from models.prescription.typ.medication.routes.topical import Topical
from models.prescription.typ.medication.routes.transdermal import Transdermal
from models.prescription.typ.medication.routes.vaginal import Vaginal
from models.prescription.typ.psychotherapy.psychotherapies.cognitive import (
    CognitiveBehavioralTherapy)
from models.prescription.typ.psychotherapy.psychotherapies.family import (
    FamilyGroupTherapy)
from models.prescription.typ.psychotherapy.psychotherapies.humanistic import (
    HumanisticTherapy)
from models.prescription.typ.psychotherapy.psychotherapies.interpersonal import (
    InterpersonalTherapy)
from models.prescription.typ.psychotherapy.psychotherapies.psychodynamic import (
    PsychoDynamicTherapy)
from models.prescription.typ.psychotherapy.psychotherapy import Psychotherapy
from models.prescription.types_class import PrescribableItemType
from models.saa import Saa
from models.schedule import Schedule
from models.severity import Severity
from models.slot import Slot
from models.span import Span
from models.user import User


from models.proxy.practitioners.clinical_officer import ClinicalOfficer
from models.proxy.practitioners.dentist import Dentist
from models.proxy.practitioners.dietitian import Dietitian
from models.proxy.practitioners.doctor import Doctor
from models.proxy.practitioners.lab_tech import LabTech
from models.proxy.practitioners.nurse import Nurse
from models.proxy.practitioners.pharmacist import Pharmacist
from models.proxy.practitioners.physiotherapist import Physiotherapist
from models.proxy.practitioners.psychologist import Psychologist
from models.proxy.users.adult import Citizen
from models.proxy.users.child import Child

# import os


classes = {
    "AdministrationRoute": AdministrationRoute,
    "AdultProfile": AdultProfile,
    "Appointment": Appointment,
    "BreastCancer": BreastCancer, "Buccal": Buccal,
    "Child": Child, "ChildProfile": ChildProfile,
    "Citizen": Citizen, "ClinicalOfficer": ClinicalOfficer,
    "CognitiveBehavioralTherapy": CognitiveBehavioralTherapy,
    "ColorectalCancer": ColorectalCancer,
    "Date": Date, "DermalImplant": DermalImplant,
    "Dentist": Dentist, "Diagnosis": Diagnosis,
    "DiagnosticCategory": DiagnosticCategory, "DiagnosticTest": DiagnosticTest,
    "Dietitian": Dietitian, "Doctor": Doctor, "DoctorNote": DoctorNote,
    "FamilyGroupTherapy": FamilyGroupTherapy,
    "FeedingTube": FeedingTube,
    "Frequency": Frequency, "HealthProgram": HealthProgram,
    "HumanisticTherapy": HumanisticTherapy,
    "Infusion": Infusion, "Inhalation": Inhalation,
    "Injection": Injection,
    "InterpersonalTherapy": InterpersonalTherapy, "Intramuscular": Intramuscular,
    "Intravenous": Intravenous,
    "LabTech": LabTech,
    "Leukemia": Leukemia,
    "LogInfo": LogInfo, "LungCancer": LungCancer,
    "Lymphoma": Lymphoma,
    "Nasal": Nasal,
    "Nurse": Nurse, "Ophthalmic": Ophthalmic, "Oral": Oral,
    "Otic": Otic, "PatientPrescription": PatientPrescription,
    "Pharmacist": Pharmacist,
    "Physiotherapist": Physiotherapist, "Planner": Planner,
    "PracProfile": PracProfile, "PractitionerProgram": PractitionerProgram,
    "PrescribableItemType": PrescribableItemType,
    "PrescriptionEntry": PrescriptionEntry,
    "PsychoDynamicTherapy": PsychoDynamicTherapy, "Psychotherapy": Psychotherapy,
    "Psychologist": Psychologist, "Rectal": Rectal, "Saa": Saa,
    "Severity": Severity, "Schedule": Schedule, "Slot": Slot, "Span": Span,
    "Subcutaneous": Subcutaneous, "Sublingual": Sublingual,
    "TestOrder": TestOrder, "TestOrderTestLink": TestOrderTestLink,
    "Topical": Topical,
    "Transdermal": Transdermal, "User": User,
    "Vaginal": Vaginal
}


class DBStorage:

    def __init__(self):
        """Instantiate a DBStorage object
        if os.getenv('FLASK_ENV') == "test":
            db.drop_all()
        """

    def all(self, _cls=None):
        """Queries on the current database session to retrieve class instances

            Args:
                _cls (str): Name of the Model to retrieve its instance(s) present
                            in the database.
                            If _cls in None, then all database entries are
                            returned. This is a very expensive transaction and
                            should be avoided, especially when the database have
                            several entries.
            Returns:
                dict: Key/Value represntation of the Model instance attribute
                            values.

        """
        if _cls and _cls not in classes.values():
            raise ValueError(f"Invalid model class: {_cls}")

        new_dict = {}
        for class_name, class_type in classes.items():
            if _cls is None or _cls == class_type or _cls == class_name:
                try:
                    objs = db.session.query(class_type).all()
                    for obj in objs:
                        key = f"{obj.__class__.__name__}.{obj.id}"
                        new_dict[key] = obj
                except Exception as e:
                    raise RuntimeError(f"Failed to query objects for {class_name}: {e}")
        return (new_dict)

    def new(self, obj):
        """Adds the object to the current database session.

            Args:
                obj (str): The new object to be added into the database.
        """
        db.session.add(obj)

    def save(self):
        """Commits all changes of the current database session"""
        db.session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None

            Args:
                obj (str): The object/Model instance to be deleted from the database
        """
        if obj is not None:
            db.session.delete(obj)

    def close(self):
        """Calls remove() method on the private session attribute"""
        db.session.remove()

    def get(self, _cls, _id):
        """
        Gets the object based on the class name and its ID, or
            None if not found.

        Args:
            _cls (str): A model name.
            _id (str): The id of the model instance to be retrived.

        Returns:
            obj: An object instance matching the id passed, else None.
        """
        model_class = _cls if isinstance(_cls, type) else classes.get(_cls)
        if not model_class:
            raise ValueError(f"Class '{_cls}' not found !")

        try:
            obj = db.session.get(model_class, _id)
            return obj
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve objects for '{_cls}': {e}")

        return None

    def count(self, _cls=None):
        """Counts the number of Model instances in the database

           Args:
            _cls (str): The Model to count instances of.

           Returns:
            int: The total count of specied Model instance entries.
                If _cls is None then it returns all Models' entry count.This is
                too expensive transaction. Please avoid unless really required.
        """
        if _cls is None:
            return sum(db.session.query(cls).count() for cls in classes.values())
        else:
            model_class = _cls if isinstance(_cls, type) else classes.get(_cls)
            if not model_class:
                raise ValueError(f"Class '{_cls}' not found!")
            return db.session.query(model_class).count()
