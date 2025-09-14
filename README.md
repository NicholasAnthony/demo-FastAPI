# demo-FastAPI

A small demo application showing user registration and login using FastAPI, Pydantic models, password hashing, and SQLite storage.

Features
- API endpoints:
	- `POST /register` — register a new user (JSON body: `username`, `password`, `email`)
	- `POST /login` — login and receive a short-lived bearer token (JSON body: `username`, `password`)
	- `GET /me` — protected API endpoint that returns the current user's `username` and `email` (requires `Authorization: Bearer <token>`)
- SQLite database using SQLAlchemy ORM (`models_db.py`, `db.py`)
- Password hashing with `passlib` (bcrypt)
- Token storage (random token strings) in the database with expiry
- Simple web GUI using Jinja2 templates and static CSS:
	- `/` landing page
	- `/register` (form)
	- `/login` (form)
	- `/profile` (profile page showing logged-in user)

Requirements
- Python 3.10+ (this project was tested in a virtualenv)
- See `requirements.txt` for exact pinned packages

Quick start (PowerShell)
1. Activate your virtual environment (or create one):

```powershell
# create venv (if you don't have one)
python -m venv .venv
& .venv\Scripts\Activate.ps1

# install deps
python -m pip install -r requirements.txt
```

2. Run the app (default port 8000):

```powershell
& .venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

3. Open the GUI in your browser:

- `http://127.0.0.1:8000/` — landing page
- `http://127.0.0.1:8000/register` — register form
- `http://127.0.0.1:8000/login` — login form
- `http://127.0.0.1:8000/profile` — profile (reads token cookie set on login)


Notes & next steps
- This demo stores tokens as random strings in the database. For production use, switch to JWTs (PyJWT) or OAuth2 flows and use HTTPS.
- Consider adding logout, email verification, password reset, rate limiting, and stronger session management for a real app.

License
- This project is a small demo. Use and modify as you see fit.

