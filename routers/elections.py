from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from models import User, Category, Vote, Election
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from datetime import datetime

templates = Jinja2Templates(directory="templates")
router = APIRouter()





def get_admin_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    is_admin = request.session.get("is_admin", False)
    if not user_id or not is_admin:
        return None
    user = db.query(User).filter(User.id == user_id, User.is_admin == True).first()
    return user

@router.get("/noticeBoard")
def register_get(request: Request):
    return templates.TemplateResponse("notice_board.html", {"request": request})


@router.get("/admin/elections")
def admin_elections(request: Request, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    if not admin:
        return RedirectResponse("/auth/login", status_code=302)

    elections = db.query(Election).order_by(Election.start_date.desc()).all()
    categories = db.query(Category).all()
    return templates.TemplateResponse("admin_election.html", {
        "request": request,
        "elections": elections,
        "categories": categories
    })


@router.post("/admin/elections/schedule")
def schedule_election(
    category_id: int = Form(...),
    start_time: str = Form(...),
    end_time: str = Form(...),
    db: Session = Depends(get_db),
    admin=Depends(get_admin_user)
):
    if not admin:
        return RedirectResponse("/auth/login", status_code=302)
    
    if not category_id:
         return RedirectResponse("/admin/elections", status_code=302)

    category = db.query(Category).filter(Category.id == int(category_id)).first()
    if not category:
        return RedirectResponse("/admin/elections", status_code=302)

    # Title derived from category
    title = f"{category.name} Election"

    start_dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
    end_dt = datetime.strptime(end_time, "%Y-%m-%dT%H:%M")

    election = Election(
        title=title,
        category_id=category_id,
        start_time=start_dt,
        start_date=start_dt,
        end_time=end_dt,
        end_date=end_dt,
        is_active=True
    )
    db.add(election)
    db.commit()
    return RedirectResponse("/admin/elections", status_code=303)

