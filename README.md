# CLI Health Information System
 ## Overview
This is a Command-Line Interface (CLI) Health Information System developed to manage patient-practitioner interactions and the management of patient-related data. It provides a secure and organized way for both patients and practitioners to access, sign up for, and manage healthcare programs.
## Asumptions
The system is built on the following assumptions:
- National Registry Access: The system can retrieve adult user information (e.g., full names, date of birth, etc.) by inputting their ID number. For children, the system uses birth certificate numbers to access data.

- Practitioner Registry Integration: The system fetches practitioner data (such as name and profession type) by providing a registration number and their professional category (e.g., Nurse).

*******It is assumed the system has access to the necessary government databases and union registries for data validation and retrieval******************
## Platform

******This system is optimized for and works best on Ubuntu Linux environments.
## Accessing Start-Up Data
Startup data is stored in the following directories:

- Children’s birth certificate numbers:

`utils/proxy/data/children.py`

- Adult citizens' ID numbers:

`utils/proxy/data/citizens.py`

- Practitioners’ registration IDs and profession types:

`utils/proxy/data/practitioners`

These datasets are necessary to successfully register and authenticate users into the system.
## Running The Program
To start the system, follow these steps:

1. Start the API server

Run the following file from project root:

`./api/v1/app.py`

To start the project's local server to allow for API calls

2. Launch the CLI

Start the CLI using:

`python3 main.py`

**NOTE**: Once in the CLI, **Double-click**** every input to ensure proper CLI interaction.
## System Features
Upon startup, the CLI system offers a variety of features and workflows:
### Practitioner Features
- Sign in, sign out, and create an account.
- View all available healthcare programs.
- Link (sign up) to existing programs.
- View a list of all assigned patients.

********Practitioners can only view patients that are assigned to them.*************

### Patient Features
- Sign in, sign out, and create an account.
- View all available healthcare programs.
- Sign up for healthcare programs directly.
- Choose a preferred practitioner when signing up.
- Automatically receive a booked appointment with the selected practitioner.
- View all personal appointments.

### Shared Features
**Role-based access control:**
Upon sign-in, users are routed to their respective dashboards:

1. `Adults → Adult Menu`
2. `Practitioners → Practitioner Menu`

## Tech Stack
```
Language: Python
Backend: Flask (for REST API)
Database ORM: SQLAlchemy
Documentation & Style:
    Codebase is written following Google-style documentation for clarity and consistency.
All development was done in VIM, the developer's preferred code editor.
```
