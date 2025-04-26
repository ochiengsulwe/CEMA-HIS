import click
import requests
import os

API_URL = os.getenv('CEMA_HIS_API_CLI_URL', 'http://localhost:5000/#/')
TOKEN_FILE = '.mordi_token'


def save_token(token):
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)


def get_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as f:
            return f.read().strip()
    return None


def auth_headers():
    token = get_token()
    return {'Authorization': f'Bearer {token}'} if token else {}


@click.group()
def cli():
    """Dokta Mordi CLI: Manage your healthcare platform via terminal"""
    pass


@cli.command()
@click.argument('email')
@click.argument('password')
def login(email, password):
    """Login as a user (stores JWT token locally)"""
    response = requests.post(f'{API_URL}/auth/login', json={
        'email': email,
        'password': password
    })
    if response.ok:
        token = response.json().get('access_token')
        save_token(token)
        click.echo('Login successful')
    else:
        click.echo(f'Login failed: {response.text}')


@cli.command()
@click.argument('email')
@click.argument('password')
@click.argument('first_name')
@click.argument('last_name')
def register(email, password, first_name, last_name):
    """Register a new user"""
    response = requests.post(f'{API_URL}/auth/register', json={
        'email': email,
        'password': password,
        'first_name': first_name,
        'last_name': last_name
    })
    if response.ok:
        click.echo('Registration successful')
    else:
        click.echo(f'Registration failed: {response.text}')


@cli.command()
@click.argument('prac_id')
@click.argument('program_id')
@click.argument('date')
@click.argument('time_from')
@click.argument('time_to')
def book_adult(prac_id, program_id, date, time_from, time_to):
    """Book an adult appointment"""
    payload = {
        'practitioner_id': prac_id,
        'program_id': program_id,
        'date': date,
        'time_from': time_from,
        'time_to': time_to
    }
    response = requests.post(f'{API_URL}/appointments/adult/book',
                             headers=auth_headers(),
                             json=payload)
    if response.ok:
        click.echo('Appointment booked')
    else:
        click.echo(f'Booking failed: {response.text}')

# Add more commands for planner creation, child booking, etc.


if __name__ == '__main__':
    cli()
