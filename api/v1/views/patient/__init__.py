from flask import Blueprint

patient = Blueprint('patient', __name__)
from api.v1.views.patient.appointment.adult.all_appointments import (
        all_adult_appointments)
from api.v1.views.patient.appointment.adult.book import book_adult_appointment
from api.v1.views.patient.appointment.adult.cancel import cancel_adult_appointment
from api.v1.views.patient.appointment.adult.completed import complete_appointments
from api.v1.views.patient.appointment.adult.one_appointment import (
        one_adult_appointment)
from api.v1.views.patient.appointment.adult.reschedule import (
        reschedule_adult_appointment)
from api.v1.views.patient.appointment.adult.schedule import one_adult_schedule
from api.v1.views.patient.appointment.adult.upcoming import upcoming_appointment
from api.v1.views.patient.appointment.child.all_appointments import (
    all_child_appointments)
from api.v1.views.patient.appointment.child.book import book_child_appointment
from api.v1.views.patient.appointment.child.cancel import cancel_child_appointment
from api.v1.views.patient.appointment.child.completed import complete_c_appointments
from api.v1.views.patient.appointment.child.one_appointment import (
    one_child_appointment)
from api.v1.views.patient.appointment.child.reschedule import (
    reschedule_child_appointment)
from api.v1.views.patient.appointment.child.schedule import one_child_schedule
from api.v1.views.patient.appointment.child.upcoming import upcoming_c_appointment
from api.v1.views.patient.diagnosis.adult.all import all_adult_diagnoses
from api.v1.views.patient.diagnosis.adult.one import this_adult_diagnosis
from api.v1.views.patient.diagnosis.child.all import all_child_diagnoses
from api.v1.views.patient.diagnosis.child.one import this_child_diagnosis
from api.v1.views.patient.prescription.adult.all import all_adult_prescriptions
from api.v1.views.patient.prescription.adult.cancelled import (
    all_cancelled_adult_prescriptions)
from api.v1.views.patient.prescription.adult.fulfilled import (
    all_fulfilled_adult_prescriptions)
from api.v1.views.patient.prescription.adult.issued import (
    all_issued_adult_prescriptions)
from api.v1.views.patient.prescription.adult.one import this_adult_prescription
from api.v1.views.patient.prescription.adult.received import (
    all_received_adult_prescriptions)
from api.v1.views.patient.prescription.child.all import all_child_prescriptions
from api.v1.views.patient.prescription.child.cancelled import (
    all_cancelled_child_prescriptions)
from api.v1.views.patient.prescription.child.fulfilled import (
    all_fulfilled_child_prescriptions)
from api.v1.views.patient.prescription.child.issued import (
    all_issued_child_prescriptions)
from api.v1.views.patient.prescription.child.one import this_child_prescription
from api.v1.views.patient.prescription.child.received import (
    all_received_child_prescriptions)
from api.v1.views.patient.program.adult.my_progs import all_adult_programs
from api.v1.views.patient.program.adult.this_pog import this_adult_program
from api.v1.views.patient.program.child.my_progs import all_child_programs
from api.v1.views.patient.program.child.this_pog import this_child_program
from api.v1.views.patient.program.all import retrieve_for_patient_programs
from api.v1.views.patient.program.one import this_program_for_patient
