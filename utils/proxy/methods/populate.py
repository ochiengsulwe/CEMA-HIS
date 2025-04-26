from datetime import datetime


def populate_from_data(model_class, data_list, session):
    """Populates instances of a SQLAlchemy model class with data from
            a list of dictionaries.

    Args:
        model_class (class): The SQLAlchemy model class to populate
            (e.g., Nurse, Doctor).
        data_list (:obj: `list` of :obj: `dict`): List of dictionaries where each
            dictionary contains attribute data for a single instance of model_class.
        session (session): SQLAlchemy session object to use for adding
            instances and committing changes.

    Notes:
        This function iterates over data_list and creates an instance of model_class
            for each dictionary.
        It dynamically assigns values to attributes of model_class based on keys in
            each dictionary.
        Date attributes ('reg_year', 'spec_year') are expected to be in '%Y-%m-%d'
            format and are parsed using datetime.strptime() before assignment.

    Example:
        Assuming a Nurse model and SQLAlchemy session:
        nurses_data = [
            {'id_num': 801, 'first_name': 'Alice', 'last_name': 'Smith',
                'license_num': 'N123456', 'reg_year': '2015-06-20'},
            {'id_num': 802, 'first_name': 'Bob', 'middle_name': 'M',
                'last_name': 'Johnson', 'license_num': 'N234567',
                'reg_year': '2018-07-15'},
            {'id_num': 803, 'first_name': 'Carol', 'last_name': 'Brown',
                'license_num': 'N345678', 'reg_year': '2016-08-10',
                'specialization': 'Emergency Nursing', 'spec_reg_num': 'EN345',
                'spec_year': '2019-09-25'},
        ]
        `populate_from_data(Nurse, nurses_data, db.session)`
    """

    for data in data_list:
        query = session.query(model_class)
        if hasattr(model_class, 'id_num') and 'id_num' in data:
            query = session.query(
                model_class).filter(model_class.id_num == data['id_num'])

        if hasattr(model_class, 'birth_cert_number') and 'birth_cert_number' in data:
            query = session.query(
                    model_class).filter(
                        model_class.birth_cert_number == data['birth_cert_number'])

        if hasattr(
                model_class, 'registration_number') and 'registration_number' in data:
            query = session.query(
                    model_class).filter(
                        model_class.registration_number == data['registration_number'])

        if hasattr(model_class, 'name') and 'name' in data:
            query = session.query(model_class).filter(model_class.name == data['name'])

        if hasattr(model_class, 'symptom') and 'symptom' in data:
            query = session.query(model_class).filter(
                model_class.symptom == data['symptom'])

        if hasattr(model_class, 'side') and 'side' in data:
            query = session.query(model_class).filter(model_class.side == data['side'])

        if hasattr(model_class, 'severity_level') and 'severity_level' in data:
            query = session.query(model_class).filter(
                model_class.severity_level == data['severity_level'])

        if hasattr(model_class, 'part') and 'part' in data:
            query = session.query(model_class).filter(model_class.part == data['part'])

        if hasattr(model_class, 'type') and 'type' in data:
            query = session.query(model_class).filter(model_class.type == data['type'])

        if hasattr(model_class, 'code') and 'code' in data:
            query = session.query(model_class).filter(model_class.code == data['code'])

        if hasattr(model_class, 'id') and 'id' in data:
            query = session.query(model_class).filter(model_class.id == data['id'])

        if query.first():
            continue

        instance = model_class()
        for key, value in data.items():
            if hasattr(instance, key):
                if key in ['reg_year', 'spec_year', 'date_of_birth']:
                    setattr(
                            instance, key, datetime.strptime(
                                value, '%Y-%m-%d').date() if value else None)
                else:
                    setattr(instance, key, value)
        try:
            session.add(instance)
        except Exception as e:
            print(f"Error adding {data['name'] if 'name' in data else 'unknown'}: {e}")
            session.rollback()
            continue
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error committing session: {e}")


def populate_diagnostic_data(session, models_with_data):
    """
    Populates SQLAlchemy models with data and maintains relationships dynamically.

    Args:
        session (Session): SQLAlchemy session instance.
        models_with_data (dict): Dictionary where keys are model classes and
                                 values are lists of dictionaries representing data.

    Example:
        models_with_data = {
            DiagnosticCategory: [
                {'name': 'Laboratory Tests'},
                {'name': 'Imaging Tests'}
            ],
            DiagnosticTest: [
                {'name': 'Complete Blood Count (CBC)', 'test_for': 'Infections, anemia',
                'category_name': 'Laboratory Tests'},
                {'name': 'X-ray', 'test_for': 'Bone fractures',
                'category_name': 'Imaging Tests'}
            ]
        }
        populate_diagnostic_data(db.session, models_with_data)
    """
    from models.diagnostics.category import DiagnosticCategory
    from models.diagnostics.test import DiagnosticTest
    instances = {}  # Store created instances for relationships

    # Insert main records (Categories first)
    for model_class, data_list in models_with_data.items():
        if model_class == DiagnosticCategory:
            for data in data_list:
                unique_keys = ["name"]
                filters = {key: data[key] for key in unique_keys if key in data}

                existing_instance = session.query(
                    model_class).filter_by(**filters).first()
                if existing_instance:
                    instances.setdefault(model_class, []).append(existing_instance)
                    continue

                instance = model_class(**data)
                session.add(instance)
                instances.setdefault(model_class, []).append(instance)

    session.commit()

    # Insert Diagnostic Tests with proper category_id
    for model_class, data_list in models_with_data.items():
        if model_class == DiagnosticTest:
            for data in data_list:
                category_name = data.pop("category_name", None)
                category_instance = session.query(
                    DiagnosticCategory).filter_by(name=category_name).first()

                if not category_instance:
                    print(
                        f"Error: Category '{category_name}' not "
                        f"found for test '{data['name']}'"
                    )
                    continue  # Skip this test if category is missing

                data["category_id"] = category_instance.id  # Assign correct foreign key

                instance = model_class(**data)
                session.add(instance)
                instances.setdefault(model_class, []).append(instance)

    try:
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error committing session: {e}")
