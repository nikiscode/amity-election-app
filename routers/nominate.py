# routes/nominate.py

from fastapi import APIRouter, Request, Form, UploadFile, File, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import shutil

from sqlalchemy.orm import Session
from database import get_db
from models import User, Category, Candidate,Election
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="templates")

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


@router.get("/nominate")
def get_nominate_form(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    now = datetime.utcnow()
    elections = db.query(Election).filter(
        Election.is_active == True,
        Election.end_date >= now
    ).all()

    return templates.TemplateResponse("nominate.html", {
        "request": request,
        "user_name": user.name,
        "elections": elections
    })

@router.post("/nominate")
async def post_nominate(
    request: Request,
    name: str = Form(...),
    election_id: int = Form(...),
    slogan: str = Form(...),
    symbol_image: UploadFile = File(...),
    video: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=303)

    # Save uploaded files
    symbol_filename = f"symbol_{user_id}_{symbol_image.filename}"
    symbol_path = f"static/uploads/symbols/{symbol_filename}"
    with open(symbol_path, "wb") as buffer:
        shutil.copyfileobj(symbol_image.file, buffer)

    video_filename = f"video_{user_id}_{video.filename}"
    video_path = f"static/uploads/videos/{video_filename}"
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)

    # Create candidate record
    candidate = Candidate(
        user_id=user_id,
       election_id=election_id,
        name=name,
        slogan=slogan,
        symbol_image=f"/static/uploads/symbols/{symbol_filename}",
        video=f"/static/uploads/videos/{video_filename}",
        status='pending'
    )
    db.add(candidate)
    db.commit()

    categories = db.query(Category).all()
    message = "Nomination submitted successfully and is pending for approval."
    return templates.TemplateResponse("nominate.html", {"request": request, "categories": categories, "message": message})
