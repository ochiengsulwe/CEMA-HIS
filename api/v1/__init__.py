"""
    - this is the entrypoint for the application
    - it creates the app factory
    - it defines, configures and initializes the app object
    - it initializes applications dependencies and all blueprints
"""
from apscheduler.jobstores.base import JobLookupError

import logging
import os

from flask import Flask, jsonify, redirect, request, url_for
from flask_apscheduler import APScheduler
from flask_caching import Cache

from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
from zoneinfo import ZoneInfo

from flasgger import Swagger
from flask.logging import default_handler
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_login import current_user, LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from config.config import config
from config.swagger import swagger_config, template


db = SQLAlchemy()
moment = Moment()
migrate = Migrate()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
jwt = JWTManager()
scheduler = APScheduler()


def create_app(config_name):
    """
        Create and configure flask app intsance
        :param config_name: The configuration to use.
        :return: app instance
    """

    app = Flask(__name__)

    app.config.from_object(config[config_name])

    cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    Swagger(app, config=swagger_config, template=template)

    cors = CORS(app)
    # cors = CORS(app,resources={r"/api/v1/*": {"origins": "*"}})

    """
    All model classes MUST be imported here. If you don't know why CALL ME!!
    """
    from models import (
        adult_profile, appointment, base_model, child_profile, date, diagnosis,
        doctors_note, h_prog, loginfo, planner, prac_program, practitioner_profile,
        saa, schedule, severity, slot, span, token_blocklist, user
        )
    from models.diagnostics import category, link, order, test
    from models.prescription import (frequency, patient_prescription,
                                     prescription_entry, types_class)
    from models.prescription.typ.chemotherapy import chemo_type
    from models.prescription.typ.chemotherapy.chemo_types import (
        breast, colorectal, leukemia, lung, lymphoma
    )
    from models.prescription.typ.medication import route
    from models.prescription.typ.medication.routes import (
        buccal, feeding_tube, inhalation, injection, intravenous, ophthalmic, otic,
        subcutaneous, topical, vaginal, dermal_implant, infusion, intramuscular,
        nasal, oral, rectal, sublingual, transdermal
    )
    from models.prescription.typ.psychotherapy import psychotherapy
    from models.prescription.typ.psychotherapy.psychotherapies import cognitive
    from models.prescription.typ.psychotherapy.psychotherapies import family
    from models.prescription.typ.psychotherapy.psychotherapies import humanistic
    from models.prescription.typ.psychotherapy.psychotherapies import interpersonal
    from models.prescription.typ.psychotherapy.psychotherapies import psychodynamic
    from models.proxy.practitioners import (
            clinical_officer, dentist, dietitian, doctor, lab_tech,
            nurse, pharmacist, physiotherapist, psychologist
            )
    from models.proxy.users import adult, child
    from models.proxy.facilities import ambulance, hospital, lab, pharmacy

    initialize_extensions(app)

    with app.app_context():
        db.create_all()

        from utils.database import (
                ensure_future_dates, populate_dates, populate_time_table)
        from utils.proxy.data.citizens import register
        from utils.proxy.data.children import children_birth_data
        from utils.proxy.data.facilities.ambulances import ambulance_services
        from utils.proxy.data.facilities.hospitals import hospitals
        from utils.proxy.data.facilities.laboratories import laboratories
        from utils.proxy.data.facilities.pharmacies import pharmacies
        from utils.proxy.data.facilities.services.hospital_services import (
            medical_services)
        from utils.proxy.data.health_programs import health_programs
        from utils.proxy.data.practitioners import (
            dentists, doctors, clinical_officers, nurses, dietitians,
            lab_techs, pharmacists, physiotherapists, psychologists
        )
        from utils.proxy.data.prescription.chemo_types import chemo_types
        from utils.proxy.data.prescription.chemos import (
            breast_cancer, colorectal_cancer, leukemia_, lung_cancer, lymphoma_
        )
        from utils.proxy.data.prescription.item_types import item_types
        from utils.proxy.data.prescription.psychotherapy_types import psychotherapies
        from utils.proxy.data.prescription.psychotherapies import (
            cognitive_behavioral_therapy, family_and_group_therapy,
            humanistic_therapy, interpersonal_therapy, psychodynamic_therapy)
        from utils.proxy.data.prescription.route_data import (
            buccal_, feeding_tube_, inhalation_, injection_, intravenous_, ophthalmic_,
            otic_, subcutaneous_, topical_, vaginal_, dermal_implant_, infusion_,
            intramuscular_, nasal_, oral_, rectal_, sublingual_, transdermal_
        )
        from utils.proxy.data.prescription.routes import a_routes
        from utils.proxy.data.severities import severities
        from utils.proxy.data.tests_date import models_with_data
        from utils.proxy.methods.populate import (
            populate_from_data, populate_diagnostic_data)
        from utils.proxy.methods.populate_ import populate_from_data_

        populate_diagnostic_data(db.session, models_with_data)
        populate_from_data(adult.Citizen, register, db.session)
        populate_from_data(breast.BreastCancer, breast_cancer, db.session)
        populate_from_data(buccal.Buccal, buccal_, db.session)
        populate_from_data(chemo_type.ChemoType, chemo_types, db.session)
        populate_from_data(child.Child, children_birth_data, db.session)
        populate_from_data(clinical_officer.ClinicalOfficer,
                           clinical_officers, db.session)
        populate_from_data(
            cognitive.CognitiveBehavioralTherapy,
            cognitive_behavioral_therapy,
            db.session
        )
        populate_from_data(colorectal.ColorectalCancer, colorectal_cancer, db.session)
        populate_from_data(dentist.Dentist, dentists, db.session)
        populate_from_data(dermal_implant.DermalImplant, dermal_implant_, db.session)
        populate_from_data(dietitian.Dietitian, dietitians, db.session)
        populate_from_data(doctor.Doctor, doctors, db.session)
        populate_from_data(
            family.FamilyGroupTherapy,
            family_and_group_therapy,
            db.session
        )
        populate_from_data(feeding_tube.FeedingTube, feeding_tube_, db.session)
        populate_from_data(h_prog.HealthProgram, health_programs, db.session)
        populate_from_data(hospital.ProxyHospital, hospitals, db.session)
        populate_from_data(
            humanistic.HumanisticTherapy,
            humanistic_therapy,
            db.session
        )
        populate_from_data(infusion.Infusion, infusion_, db.session)
        populate_from_data(inhalation.Inhalation, inhalation_, db.session)
        populate_from_data(injection.Injection, injection_, db.session)
        populate_from_data(
            interpersonal.InterpersonalTherapy,
            interpersonal_therapy,
            db.session
        )
        populate_from_data(intramuscular.Intramuscular, intramuscular_, db.session)
        populate_from_data(intravenous.Intravenous, intravenous_, db.session)
        populate_from_data(lab.ProxyLaboratory, laboratories, db.session)
        populate_from_data(lab_tech.LabTech, lab_techs, db.session)
        populate_from_data(leukemia.Leukemia, leukemia_, db.session)
        populate_from_data(lung.LungCancer, lung_cancer, db.session)
        populate_from_data(lymphoma.Lymphoma, lymphoma_, db.session)
        populate_from_data(nasal.Nasal, nasal_, db.session)
        populate_from_data(nurse.Nurse, nurses, db.session)
        populate_from_data(ophthalmic.Ophthalmic, ophthalmic_, db.session)
        populate_from_data(oral.Oral, oral_, db.session)
        populate_from_data(otic.Otic, otic_, db.session)
        populate_from_data(pharmacist.Pharmacist, pharmacists, db.session)
        populate_from_data(pharmacy.ProxyPharmacy, pharmacies, db.session)
        populate_from_data(physiotherapist.Physiotherapist, physiotherapists,
                           db.session)
        populate_from_data(
            psychodynamic.PsychoDynamicTherapy,
            psychodynamic_therapy,
            db.session
        )
        populate_from_data(psychotherapy.Psychotherapy, psychotherapies, db.session)
        populate_from_data(psychologist.Psychologist, psychologists, db.session)
        populate_from_data(rectal.Rectal, rectal_, db.session)
        populate_from_data(route.AdministrationRoute, a_routes, db.session)
        populate_from_data(severity.Severity, severities, db.session)
        populate_from_data(subcutaneous.Subcutaneous, subcutaneous_, db.session)
        populate_from_data(sublingual.Sublingual, sublingual_, db.session)
        populate_from_data(topical.Topical, topical_, db.session)
        populate_from_data(transdermal.Transdermal, transdermal_, db.session)
        populate_from_data(types_class.PrescribableItemType, item_types, db.session)
        populate_from_data(vaginal.Vaginal, vaginal_, db.session)

        populate_dates(db.session, date.Date)

        populate_time_table(db.session, saa.Saa)
        """
        populate_from_data_(medicine.Medicine, medicines, db.session)
        populate_from_data_(medical_service.MedicalService, medical_services,
                            db.session)
        populate_from_data_(test.Test, tests, db.session)
        """
    @jwt.unauthorized_loader
    def custom_unauthorized_response(callback):
        return jsonify({"error": "unauthorized, please log in"}), 401

    @jwt.token_in_blocklist_loader
    def check_if_token_is_revoked(jwt_header, jwt_payload):
        """Check if token is in blocklist (i.e., logged out)."""
        from models.token_blocklist import TokenBlocklist
        jti = jwt_payload["jti"]
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    @login_manager.user_loader
    def load_user(loginfo_id):
        return loginfo.LogInfo.query.get(str(loginfo_id))

    @app.before_request
    def initialize_cache():
        if not cache.get('dates_cached'):
            populate_dates(db.session, date.Date)
            cache.set('dates_cached', True, timeout=60 * 60 * 24 * 365)

        if not cache.get('times_cached'):
            populate_time_table(db.session, saa.Saa)
            cache.set('times_cached', True, timeout=60 * 60 * 24 * 365)

    @app.before_request
    def start_scheduler():
        def wrapper_populate_dates():
            populate_dates(db.session, date.Date)

        if not scheduler.running:
            job = scheduler.get_job('update_dates')
            if job:
                scheduler.reschedule_job(job_id='update_dates',
                                         trigger='interval', days=1)
        else:
            scheduler.add_job(
                    id='update_dates',
                    func=wrapper_populate_dates,
                    trigger='interval',
                    days=1
                    )

    configure_logging(app)

    register_blueprints(app)

    register_error_handlers(app)

    return app


def register_blueprints(app):
    from api.v1.views.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    from api.v1.views.general import get_all
    app.register_blueprint(get_all, url_prefix='/all')

    from api.v1.views.patient import patient
    app.register_blueprint(patient, url_prefix='/patient')

    from api.v1.views.practitioner import practitioner
    app.register_blueprint(practitioner, url_prefix='/practitioner')


def initialize_extensions(app):
    db.init_app(app)
    moment.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    jwt.init_app(app)


def register_error_handlers(app):
    from api.v1.views import errors
    app.register_blueprint(errors)


def configure_logging(app):
    app.logger.removeHandler(default_handler)
    custom_file_handler = RotatingFileHandler(
        "logs/api.log", maxBytes=16384, backupCount=3
    )

    custom_file_handler.setLevel(logging.INFO)

    logs_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s ["
        "in %(module)s %(filename)s: %(lineno)d]"
    )
    logs_formatter.converter = tz_converter()
    custom_file_handler.setFormatter(logs_formatter)

    app.logger.handlers.clear()
    app.logger.addHandler(custom_file_handler)


def tz_converter():
    """timezone converter for logging

    Returns:
        tuple: local time tuple
    """
    converter = datetime.now(tz=ZoneInfo("Africa/Nairobi")).timetuple()

    return converter
