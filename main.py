import json
import requests
import os
import sys

TOKEN_FILE = '.cema_token'
SESSION_FILE = '.session_data'
API_URL = 'http://localhost:5000'
SESSION_TEMPLATES = {
    'adult': {
        'user_type': None,
        'program_id': None,
        'practitioner_id': None,
        'child_id': None,
        'appointment_id': None,
    },
    'practitioner': {
        'user_type': None,
        'program_id': None,
        'patient_id': None,
        'planner_id': None,
        'slot_id': None,
        'span_id': None,
        'schedule_id': None,
        'appointment_id': None,
    },
}


def clear_input_buffer():
    while True:
        ch = sys.stdin.read(1)
        if ch == '\n' or ch == '':
            break


def safe_input(prompt):
    user_input = input(prompt)
    clear_input_buffer()
    return user_input


def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)


def clear_token():
    with open(TOKEN_FILE, 'w') as f:
        f.write('')


def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    return None


def save_session_data(data):
    with open(SESSION_FILE, 'w') as f:
        json.dump(data, f)


def clear_session_data():
    with open(SESSION_FILE, 'w') as f:
        json.dump({}, f)


def get_session_data():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, 'r') as f:
            return json.load(f)
    return {}


def auth_headers():
    token = get_token()
    return {'Authorization': f'Bearer {token}'} if token else {}


def logout():
    token = get_token()

    if not token:
        print("No access token found. You are already logged out.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/auth/logout', headers=headers)

    if response.ok:
        print('Logout successful.')
        clear_token()
        clear_session_data()
    else:
        print(f'Logout failed: {response.text}')


def login():
    """
    Prompt user to choose login type first,
    then login or redirect to account creation if login fails.
    """
    user_type = safe_input("Login as:\n1. Adult\n2. Practitioner\nEnter choice (1/2): ")

    if user_type == '1':
        login_route = '/auth/login/adult'
    elif user_type == '2':
        login_route = '/auth/login/practitioner'
    else:
        print("Invalid choice. Please select 1 for adult or 2 for practitioner.")
        return

    email = safe_input("Enter your email: ")
    password = safe_input("Enter your password: ")

    response = requests.post(f'{API_URL}{login_route}', json={
        'email': email,
        'password': password
    })

    if response.ok:
        data = response.json()
        token = data.get('access_token')
        save_token(token)
        user_type = data.get('account_type')

        if user_type in SESSION_TEMPLATES:
            session_data = SESSION_TEMPLATES[user_type].copy()
            session_data['user_type'] = user_type
            save_session_data(session_data)

        print('Login successful')
    else:
        print(f'Login failed: {response.text}')
        create = input(
            "Would you like to create an account? (yes/no): "
        ).strip().lower()
        if create == 'yes':
            if user_type == '1':
                create_adult_account()
            elif user_type == '2':
                create_practitioner_account()
        else:
            print("Okay. You can try logging in again later.")
            return


def create_account():
    account_type = input(
        "Create a "
        ":\n1. Adult Acccount\n2. "
        "Practitioner Account\nEnter choice (1/2): ")
    if account_type == '1':
        create_adult_account()
    if account_type == '2':
        create_practitioner_account()
    else:
        return


def create_child_account():
    print("\n--- Creating Child Account ---")
    birth_cert_number = safe_input("Enter Child's Birth Certificate Number: ")

    token = get_token()

    if not token:
        print("No access token found. Please log in first.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'birth_cert_number': birth_cert_number
    }

    response = requests.post(f'{API_URL}/auth/create_account/child', json=payload,
                             headers=headers)

    if response.ok:
        print('Child Account created succesfully')
    else:
        print(f'failed to create child account: {response.text}')


def create_adult_account():
    """Create an adult account."""
    print("\n--- Creating Adult Account ---")
    email = safe_input("Enter your email: ")
    password = safe_input("Enter your password: ")
    phone_number = safe_input("Enter your phone number: ")
    id_number = safe_input("Enter your ID number: ")

    payload = {
        'email': email,
        'password': password,
        'phone_number': phone_number,
        'id_number': id_number
    }

    response = requests.post(f'{API_URL}/auth/create_account/adult', json=payload)

    if response.ok:
        print("Adult account created successfully. You can now login!")
    else:
        print(f"Failed to create adult account: {response.text}")


def create_practitioner_account():
    """Create a practitioner account."""
    print("\n--- Creating Practitioner Account ---")
    email = safe_input("Enter your email: ")
    password = safe_input("Enter your password: ")
    phone_number = safe_input("Enter your phone number: ")
    fee = safe_input("Enter your consultation fee: ")
    profession_reg = safe_input("Enter your professional registration number: ")
    profession_type = safe_input("Enter your profession type: ")

    payload = {
        'email': email,
        'password': password,
        'phone_number': phone_number,
        'fee': fee,
        'profession_reg': profession_reg,
        'profession_type': profession_type,
    }

    response = requests.post(
        f'{API_URL}/auth/create_account/practitioner', json=payload)

    if response.ok:
        print("Practitioner account created successfully. You can now login!")
    else:
        print(f"Failed to create practitioner account: {response.text}")


def adult_menu():
    while True:
        print("\n--- Adult Menu ---")
        print("1. Book Appointment")
        print("2. View My Appointments")
        print("3. Create Child Account")
        print("4. Logout")

        choice = safe_input("Enter choice: ")

        if choice == '1':
            book_appointment()
        elif choice == '2':
            patient_appointments()
        elif choice == '3':
            create_child_account()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid option.")


def book_appointment():
    """
    Book an appointment by selecting a program, a practitioner,
        and scheduling the appointment.
    """
    token = get_token()

    if not token:
        print("You must be logged in to book an appointment.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/patient/programs/available', headers=headers)

    if response.ok:
        grouped_programs = response.json()
        if not grouped_programs:
            print("No programs available.")
            return

        print("\n--- Available Programs ---")
        program_list = []
        for program_name, program_items in grouped_programs.items():
            for program in program_items:
                program_list.append(program)
                print(f"ID: {program['id']}, Name: {program_name}, "
                      f"Description: {program['description']}")

        program_id = safe_input(
            "Enter the Program ID you want to book an appointment for: ")

        response = requests.get(
            f'{API_URL}/patient/programs/{program_id}/practitioners/all',
            headers=headers)

        if response.ok:
            practitioners_by_name = response.json()
            if not practitioners_by_name:
                print("No practitioners available for this program.")
                return

            print("\n--- Available Practitioners ---")
            practitioner_list = []
            for name, practitioner_details in practitioners_by_name.items():
                print(f"Name: {name}")
                print(f"  Cost: {practitioner_details['cost']}")
                print(f"  Profession: {practitioner_details['profession']}")
                print(
                    "  Specialization: "
                    f"{practitioner_details.get('specialization', 'N/A')}")
                practitioner_list.append({
                    "name": name,
                    "practitioner_id": practitioner_details["practitioner_id"]
                })

            practitioner_name = safe_input(
                "Enter the Practitioner Name you want to book the appointment with: ")

            selected_practitioner = next(
                (
                    p for p in practitioner_list if p["name"] == practitioner_name
                ), None)

            if not selected_practitioner:
                print("Practitioner not found. Please try again.")
                return

            practitioner_id = selected_practitioner["practitioner_id"]

            print("\n--- Booking Appointment ---")
            date = safe_input("Enter Date Desired for Apppointment(YYYY-MM-DD): ")
            time_from = safe_input("From what time(H:M): ")
            time_to = safe_input("To what Time(H:M): ")
            appointment_data = {
                "date": date,
                "time_from": time_from,
                "time_to": time_to
            }

            response = requests.post(
                f'{API_URL}/patient/{program_id}/{practitioner_id}/appointment/book',
                json=appointment_data, headers=headers)

            if response.ok:
                print("Appointment booked successfully.")
            else:
                print(f"Failed to book appointment: {response.text}")
        else:
            print(f"Failed to fetch practitioners: {response.text}")
    else:
        print(f"Failed to fetch programs: {response.text}")


def patient_appointments():
    """
    Fetch all appointments and display them for the adult user.
    """
    token = get_token()

    if not token:
        print("You must be logged in to view your appointments.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/patient/appointment/all', headers=headers)

    if response.ok:
        appointments_by_date = response.json()

        if not appointments_by_date:
            print("No appointments found.")
            return

        print("\n--- Your Appointments ---")
        for date, appointments in appointments_by_date.items():
            print(f"\nAppointments for {date}:")

            for appointment in appointments:
                print(f"\n  Appointment ID: {appointment['appointment_id']}")
                print("  Time: "
                      f"{appointment['start_time']} - {appointment['end_time']}")
                print(f"  Status: {appointment['appointment_status']}")
                print(f"  Type: {appointment['appointment_type']}")
                print(f"  State: {appointment['appointment_state']}")
                print(f"  With: {appointment['appointment_with']}")

    else:
        print(f'Failed to fetch appointments: {response.text}')


def practitioner_menu():
    while True:
        print("\n--- Practitioner Menu ---")
        print("1. My Schedule")
        print("2. My Appointments")
        print("3. Manage My Programs")
        print("4. View My Patients")
        print("5. Logout")

        choice = input("Enter choice: ")

        if choice == '1':
            prac_schedule_menu()
        elif choice == '2':
            pass
        elif choice == '3':
            prac_programs_menu()
        elif choice == '4':
            manage_patients_menu()
        elif choice == '5':
            logout()
            break
        else:
            print("Invalid option.")


def prac_programs_menu():
    while True:
        print("\n--- My Programs ---")
        print("1. View Available Programs")
        print("2. Link To A Program")
        print("3. Back to Home Menu")

        choice = safe_input("Enter choice: ")

        if choice == '1':
            get_all_programs()
        elif choice == '2':
            link_practitioner_to_program()
        elif choice == '3':
            break
        else:
            print("Invalid option.")


def get_all_programs():
    """
    Fetch and display all available programs for the practitioner.
    """
    token = get_token()

    if not token:
        print("You must be logged in to view programs.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/practitioner/programs/all', headers=headers)

    if response.ok:
        grouped_programs = response.json()
        if not grouped_programs:
            print("No programs available.")
            return

        print("\n--- Available Programs ---")
        for program_name, program_list in grouped_programs.items():
            print(f"\nProgram Name: {program_name}")
            for program in program_list:
                print(f"  ID: {program['id']}, Description: {program['description']}")
    else:
        print(f'Failed to fetch programs: {response.text}')


def link_practitioner_to_program():
    """
    Link the logged-in practitioner to a specific program.
    """
    token = get_token()

    if not token:
        print("You must be logged in to link to a program.")
        return

    program_id = safe_input("Enter the Program ID you want to link to: ").strip()

    if not program_id:
        print("Program ID cannot be empty.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.post(
        f'{API_URL}/practitioner/programs/{program_id}/create', headers=headers)

    if response.ok:
        print("Successfully linked to the program!")
    else:
        print(f"Failed to link to program: {response.text}")


def prac_appointments_menu():
    while True:
        print("\n--- Manage Appointments ---")
        print("1. View All My Appointments")
        print("2. View Appointment by ID")
        print("3. Delete Appointment")
        print("4. Manage Appointment")
        print("5. Back to Practitioner Menu")

        choice = safe_input("Enter choice: ")

        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            pass
        elif choice == '5':
            break
        else:
            print("Invalid option.")


def manage_appointment_menu():
    while True:
        print("\n--- Manage Patient Appointment ---")
        print("1. Mark Complete")
        print("2. Cancell Appointment")
        print("3. Mark Repeat")
        print("4. Back to Appointment Menu")
        print("5. Back to Home Menu")

        choice = safe_input("Enter choice: ")

        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            return
        elif choice == '5':
            break
        else:
            print("Invalid option.")


def prac_schedule_menu():
    while True:
        print("\n--- Manage My Schedule ---")
        print("1. Add Availability")
        print("2. Delete Schedule")
        print("3. Adjust Schedule")
        print("4. Back to Home Menu")

        choice = safe_input("Enter choice: ")

        if choice == '1':
            create_new_schedule()
        elif choice == '2':
            pass
        elif choice == '3':
            pass
        elif choice == '4':
            break
        else:
            print("Invalid option.")


def create_new_schedule():
    print("\n--- Creating New Availability Time ---")
    date = safe_input("Enter Availability Date(YYYY-MM-DD): ")
    time_from = safe_input("Enter From what time You Are Available(H:M): ")
    time_to = safe_input("Enter To What Time You Are Available(H:M): ")

    token = get_token()

    if not token:
        print("No access token found. Please log in first.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        'date': date,
        'time_from': time_from,
        'time_to': time_to
    }

    response = requests.post(f'{API_URL}/practitioner/planner/create', json=payload,
                             headers=headers)

    if response.ok:
        print('Availability created succesfully')
    else:
        print(f'failed to add availability: {response.text}')


def manage_patients_menu():
    while True:
        print("\n--- Manage Patients ---")
        print("1. View All My Patients")
        print("2. View Patient by ID")
        print("5. Back to Home Menu")

        choice = input("Enter choice: ")

        if choice == '1':
            get_all_patients()
        elif choice == '2':
            pass
        elif choice == '3':
            break
        else:
            print("Invalid option.")


def get_all_patients():
    """
    Fetch and display all patients for the practitioner, grouped by name.
    """
    token = get_token()

    if not token:
        print("You must be logged in to view patients.")
        return

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(f'{API_URL}/practitioner/patient/all', headers=headers)

    if response.ok:
        patients_by_name = response.json()

        if not patients_by_name:
            print("No patients found.")
            return

        print("\n--- Available Patients ---")
        for name, patient_details in patients_by_name.items():
            print(f"\nName: {name}")
            for detail in patient_details:
                print(f"  Age: {detail['age']}, Gender: {detail['gender']}")
                print(f"  Program: {detail['program_in']}")
                print(f"  Loginfo ID: {detail['loginfo_id']}")
                print(f"  Account Type: {detail['type']}")

    else:
        print(f"Failed to fetch patients: {response.text}")


def main():
    print("Welcome to CEMA-HIS CLI")
    while True:
        print("\nSelect an option:")
        print("1. Login")
        print("2. Create Account")
        print("3. Quit")

        choice = safe_input("Enter choice: ")

        if choice == '1':
            login()
            session_data = get_session_data()
            if session_data:
                user_type = session_data.get('user_type')
                if user_type == 'adult':
                    adult_menu()
                elif user_type == 'practitioner':
                    practitioner_menu()
        elif choice == '2':
            create_account()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
