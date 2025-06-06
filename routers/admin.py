from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from models import User, Candidate, Election
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from collections import defaultdict
from datetime import datetime


templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="/admin")
ADMIN_EMAILS = ["admin@amity.edu"]

def get_admin_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    is_admin = request.session.get("is_admin", False)
    if not user_id or not is_admin:
        return None
    user = db.query(User).filter(User.id == user_id, User.is_admin == True).first()
    return user


@router.get("/candidates")
def admin_candidates_approval_page(request: Request, admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    if not admin:
        return RedirectResponse("/auth/login", status_code=302)

    # Get elections that are active or upcoming (optional: adjust as needed)
    now = datetime.utcnow()
    elections = db.query(Election).filter(
        Election.is_active == True,
        Election.end_time >= now
    ).all()

    elections_candidates = []
    for election in elections:
        candidates = db.query(Candidate).filter(
            Candidate.election_id == election.id,
            Candidate.status == "pending"
        ).all()

        elections_candidates.append({
            "election": election,
            "candidates": candidates
        })

    return templates.TemplateResponse("admin_candidates.html", {
        "request": request,
        "elections_candidates": elections_candidates
    })



@router.post("/candidates/action")
async def candidate_action(request: Request, action: str = Form(...), candidate_id: int = Form(...), admin=Depends(get_admin_user), db: Session = Depends(get_db)):
    if not admin:
        return RedirectResponse("/auth/login", status_code=302)

    if action not in ["approved", "rejected", "withdrawed"]:
        return RedirectResponse("/candidates", status_code=303)

    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate:
        candidate.status = action
        db.commit()
    return RedirectResponse("/candidates", status_code=302)


@router.post("/candidates/{candidate_id}/approve")
def approve_candidate(candidate_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    if not admin:
        return RedirectResponse("/auth/login", status_code=302)
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate:
        candidate.status = "approved"
        db.commit()
    return RedirectResponse("/admin/candidates", status_code=302)

@router.post("/candidates/{candidate_id}/reject")
def reject_candidate(candidate_id: int, db: Session = Depends(get_db), admin=Depends(get_admin_user)):
    if not admin:
        return RedirectResponse("/auth/login", status_code=302)
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    if candidate:
        candidate.status = "rejected"
        db.commit()
    return RedirectResponse("/admin/candidates", status_code=302)
