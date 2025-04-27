import json
import requests
import os

TOKEN_FILE = '.cema_token'
SESSION_FILE = '.session_data'

API_URL = 'http://localhost:5000'


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
    else:
        print(f'Logout failed: {response.text}')


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


def login():
    """
    Prompt user to choose login type first,
    then login or redirect to account creation if login fails.
    """
    user_type = input("Login as:\n1. Adult\n2. Practitioner\nEnter choice (1/2): ")

    if user_type == '1':
        login_route = '/auth/login/adult'
    elif user_type == '2':
        login_route = '/auth/login/practitioner'
    else:
        print("Invalid choice. Please select 1 for adult or 2 for practitioner.")
        return

    email = input("Enter your email: ")
    password = input("Enter your password: ")

    response = requests.post(f'{API_URL}{login_route}', json={
        'email': email,
        'password': password
    })

    if response.ok:
        data = response.json()
        token = data.get('access_token')
        save_token(token)

        session_data = {
            'user_type': 'adult' or 'practitioner',
            'program_id': None,
            'practitioner_id': None,
        }
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


def create_child_account():
    print("\n--- Creating Child Account ---")
    birth_cert_number = input("Enter Child's Birth Certificate Number: ")

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
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    phone_number = input("Enter your phone number: ")
    id_number = input("Enter your ID number: ")

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
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    phone_number = input("Enter your phone number: ")
    fee = input("Enter your consultation fee: ")
    profession_reg = input("Enter your professional registration number: ")
    profession_type = input("Enter your profession type: ")

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

        choice = input("Enter choice: ")

        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            create_child_account()
        elif choice == '4':
            logout()
            break
        else:
            print("Invalid option.")


def practitioner_menu():
    while True:
        print("\n--- Practitioner Menu ---")
        print("1. View My Schedule")
        print("2. Manage Appointments")
        print("3. Logout")

        choice = input("Enter choice: ")

        if choice == '1':
            pass
        elif choice == '2':
            pass
        elif choice == '3':
            logout()
            break
        else:
            print("Invalid option.")


def main():
    print("Welcome to CEMA-HIS CLI")
    while True:
        print("\nSelect an option:")
        print("1. Login")
        print("2. Create Account")
        print("3. Quit")

        choice = input("Enter choice: ")

        if choice == '1':
            login()
            session_data = get_session_data()  # <-- Load session
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
