from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from database import get_db
from models import User
import config
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/register")
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register_post(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered."})

    hashed_password = bcrypt.hash(password)
    is_admin = email in config.ADMIN_EMAILS

    new_user = User(name=name, email=email, password=hashed_password, is_admin=is_admin)
    db.add(new_user)
    db.commit()
    # db.refresh(new_user)

    # request.session["user_id"] = new_user.id
    # request.session["is_admin"] = new_user.is_admin

    return RedirectResponse("/auth/login", status_code=302)

@router.get("/login")
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login_post(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user or not bcrypt.verify(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})

    request.session["user_id"] = user.id
    request.session["is_admin"] = user.is_admin
    return RedirectResponse("/", status_code=302)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/auth/login", status_code=302)
