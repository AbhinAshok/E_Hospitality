# E-Hospitality Management System

A full-stack hospitality management system with a **Python (Django)** backend API and a **React** frontend. The backend (`E_Hospitality` project, `H_app` app) exposes the data and business logic, with role-based access control defined in `permissions.py`, and the React app in `frontend/` provides the user interface.



## Features

- Appointment booking management, prescription, medical records
- Role-based permissions for different user types (see `permissions.py`; )
- REST API consumed by the React client
- Django admin for back-office management
- Responsive React UI ( e.g. Tailwind, Material UI)

## Tech Stack

| Layer    | Technology                                              |
|----------|---------------------------------------------------------|
| Backend  | Python, Django, Django REST Framework  |
| Frontend | React (Vite)                               
| Database | SQLite (development)                                    |
| Auth     | JWT / Token / Session                             |
| Config   | Environment variables via `.env`                        |

## Project Structure

```
E_Hospitality/
├── E_Hospitality/     # Django project settings and root URLs
├── H_app/             # Main Django app (models, serializers, views, URLs)
├── frontend/          # React client
├── permissions.py     # Custom permission classes / role checks
├── manage.py
├── requirements.txt
└── .env               # Local configuration (do not commit)
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+ and npm

### 1. Clone the repository

```bash
git clone https://github.com/AbhinAshok/E_Hospitality.git
cd E_Hospitality
```

### 2. Backend setup

```bash
python -m venv venv

# Windows (Git Bash)
source venv/Scripts/activate
# macOS / Linux
# source venv/bin/activate

pip install -r requirements.txt
```

Create a `.env` file in the project root (TODO: match the variable names used in `settings.py`):

```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Run migrations and start the server:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

The API runs at `http://127.0.0.1:8000/` and the admin panel at `/admin/`.

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev     
```

The app runs at `http://localhost:5173/`



```env
VITE_API_URL=http://127.0.0.1:8000/api
```


