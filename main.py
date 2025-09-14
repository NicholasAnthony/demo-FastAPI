from fastapi import FastAPI, HTTPException, Depends, Header, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from models import RegisterModel, LoginModel, UserOut, Token
import auth
import os

app = FastAPI(title="Demo FastAPI Auth")

BASE_DIR = os.path.dirname(__file__)
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Templates and static (use absolute paths so running uvicorn from other cwd still works)
templates = Jinja2Templates(directory=TEMPLATES_DIR)
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.post("/register", response_model=UserOut)
def register(payload: RegisterModel):
    try:
        user = auth.create_user(payload.username, payload.password, payload.email)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"username": user.username, "email": user.email}


@app.post("/login", response_model=Token)
def login(payload: LoginModel):
    user = auth.authenticate_user(payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = auth.create_access_token(user.username)
    return {"access_token": token, "token_type": "bearer"}


def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing authorization header")
    if not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.split(" ", 1)[1]
    user = auth.get_current_user_from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return user


@app.get("/me", response_model=UserOut)
def me(current_user: object = Depends(get_current_user)):
    return {"username": current_user.username, "email": current_user.email}


# Web GUI routes
@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register_form")
def register_form(username: str = Form(...), password: str = Form(...), email: str = Form(...)):
    try:
        auth.create_user(username, password, email)
    except ValueError:
        return RedirectResponse(url="/register?error=exists", status_code=303)
    return RedirectResponse(url="/login", status_code=303)


@app.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login_form")
def login_form(username: str = Form(...), password: str = Form(...)):
    user = auth.authenticate_user(username, password)
    if not user:
        return RedirectResponse(url="/login?error=bad", status_code=303)
    token = auth.create_access_token(user.username)
    response = RedirectResponse(url="/profile", status_code=303)
    response.set_cookie("access_token", token)
    return response


@app.get("/profile", response_class=HTMLResponse)
def profile(request: Request):
    token = request.cookies.get("access_token")
    user = None
    if token:
        user = auth.get_current_user_from_token(token)
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})

