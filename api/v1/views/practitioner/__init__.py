from flask import Blueprint

practitioner = Blueprint('practitioner', __name__)

from api.v1.views.practitioner.appointment.add_schedule import schedule_add
from api.v1.views.practitioner.appointment.all_appointments import all_pr_appointments
from api.v1.views.practitioner.appointment.cancel import cancel_pnt_appointment
from api.v1.views.practitioner.appointment.close import prac_end_appointment
from api.v1.views.practitioner.appointment.complete import mark_appointment_complete
from api.v1.views.practitioner.appointment.completed import appointments_completed
from api.v1.views.practitioner.appointment.upcoming import appointments_upcoming
from api.v1.views.practitioner.appointment.one_appointment import one_pr_appointment
from api.v1.views.practitioner.appointment.recurrent import mark_appointment_repeat
from api.v1.views.practitioner.appointment.reschedule import reschedule_pn_appointment
from api.v1.views.practitioner.patient.appointment.add_schedule import (
    schedule_add_pa)
from api.v1.views.practitioner.patient.appointment.all_appointments import (
    all_pr_pa_appointments)
from api.v1.views.practitioner.patient.appointment.cancel import (
   cancel_pnt_pa_appointment)
from api.v1.views.practitioner.patient.appointment.close import (
   prac_end_pa_appointment)
from api.v1.views.practitioner.patient.appointment.complete import (
    complete_pr_pa_appointments)
from api.v1.views.practitioner.patient.appointment.m_complete import (
    mark_pa_appointment_complete)
from api.v1.views.practitioner.patient.appointment.one_appointment import (
    patient_appointment)
from api.v1.views.practitioner.patient.appointment.pending import (
    pending_pr_pa_appointments)
from api.v1.views.practitioner.patient.appointment.recurrent import (
    mark_pa_appointment_repeat)
from api.v1.views.practitioner.patient.appointment.reschedule import (
    reschedule_pn_pa_appointment)
from api.v1.views.practitioner.patient.diagnosis.diagnose import pa_diagnose
from api.v1.views.practitioner.patient.diagnosis.one import retrieve_diagnosis
from api.v1.views.practitioner.patient.diagnostics.add_test import pa_add_tests_to_order
from api.v1.views.practitioner.patient.diagnostics.all_tests import pa_get_tests
from api.v1.views.practitioner.patient.diagnostics.creat_order import pa_create_order
from api.v1.views.practitioner.patient.diagnostics.this_test import pa_get_test
from api.v1.views.practitioner.patient.diagnostics.remove_test_from_order import (
    pa_remove_test_from_order)
from api.v1.views.practitioner.patient.manage.all import all_pr_patients
from api.v1.views.practitioner.patient.manage.one import one_pr_patient
from api.v1.views.practitioner.patient.notes.create_note import pa_create_note
from api.v1.views.practitioner.patient.notes.update_note import pa_update_note
from api.v1.views.practitioner.patient.prescription.all import get_prescriptions
from api.v1.views.practitioner.patient.prescription.delete import delete_pres_entry
from api.v1.views.practitioner.patient.prescription.input import enter_pa_prescriptions
from api.v1.views.practitioner.patient.prescription.issue import issue_pa_prescription
from api.v1.views.practitioner.patient.prescription.one import get_entry_info
from api.v1.views.practitioner.patient.prescription.prescribe import (
    create_pa_prescription)
from api.v1.views.practitioner.patient.prescription.update import update_pres_entry
from api.v1.views.practitioner.planner.clear_day import clear_practitioner_day
from api.v1.views.practitioner.planner.create import create_practitioner_planner
from api.v1.views.practitioner.planner.day_info import practitioner_day_info
from api.v1.views.practitioner.planner.days import retrieve_practitioner_days
from api.v1.views.practitioner.planner.delete_span import delete_practitioner_span
from api.v1.views.practitioner.planner.planner import retrieve_practitioner_planner
from api.v1.views.practitioner.planner.span_info import practitioner_span_info
from api.v1.views.practitioner.planner.spans import retrieve_days_spans
from api.v1.views.practitioner.planner.update import update_practitioner_planner
from api.v1.views.practitioner.programs.all import retrieve_programs
from api.v1.views.practitioner.programs.create import create_program
from api.v1.views.practitioner.programs.one import this_program
