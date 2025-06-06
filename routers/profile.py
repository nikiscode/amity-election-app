from fastapi import APIRouter, Request, Depends, File, UploadFile
from sqlalchemy.orm import Session
from database import get_db
from models import User
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
import os
import shutil

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()

@router.get("/profile")
def profile_page(request: Request, current_user: User = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse("/auth/login", status_code=302)
    return templates.TemplateResponse("profile.html", {"request": request, "user": current_user})


@router.post("/profile/upload")
async def upload_profile_image(
    request: Request,
    profile_image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        return RedirectResponse(url="/login", status_code=302)

    # Save image
    filename = f"user_{user_id}_{profile_image.filename}"
    upload_path = os.path.join("static", "uploads", "profiles", filename)

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(profile_image.file, buffer)

    user.profile_image = filename
    db.commit()

    return RedirectResponse(url="/profile", status_code=302)


