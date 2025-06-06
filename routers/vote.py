from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from database import get_db
from models import User, Candidate, Vote, Election
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse

from sqlalchemy.orm import Session
from datetime import datetime

templates = Jinja2Templates(directory="templates")
router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()

@router.get("/vote")
def vote_page(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    now = datetime.now()

    all_elections = db.query(Election).filter(Election.is_active == True).all()

    elections_data = []

    for election in all_elections:
        # Extract time part explicitly
        start_dt = election.start_time
        end_dt = election.end_time

        if not (start_dt <= now <= end_dt):
            continue

        candidates = db.query(Candidate).filter(
            Candidate.election_id == election.id,
            Candidate.status == "approved"
        ).all()

        voted = db.query(Vote).filter_by(user_id=user.id, election_id=election.id).first() is not None

        elections_data.append({
            "election": election,
            "candidates": candidates,
            "voted": voted
        })

    return templates.TemplateResponse("vote.html", {
        "request": request,
        "elections_data": elections_data,
        "voting_open": bool(elections_data),
        "user": user
    })

@router.post("/vote")
def submit_vote(request: Request, candidate_id: int = Form(...), db: Session = Depends(get_db), user=Depends(get_current_user)):
    # Get candidate and related election
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id, Candidate.status == "approved").first()
    if not candidate:
        return RedirectResponse("/vote?error=invalid_candidate", status_code=302)

    print("Candidate:", candidate)
    print("Election ID from candidate:", candidate.election_id)
    print("Election object from relationship:", candidate.election)
    # Check if voting is open for that election
    now = datetime.utcnow()
    election = candidate.election
    if not (election.is_active and election.start_time <= now <= election.end_time):
        return RedirectResponse("/vote?error=voting_closed", status_code=302)

    # Check if user already voted in this election
    existing_vote = db.query(Vote).filter_by(user_id=user.id, election_id=election.id).first()
    if existing_vote:
        return RedirectResponse("/vote?error=already_voted", status_code=302)

    try:
        # Record the vote
        vote = Vote(user_id=user.id, candidate_id=candidate.id, election_id=election.id)
        db.add(vote)
        db.commit()
        return RedirectResponse("/vote?success=vote_recorded", status_code=302)
    except Exception as e:
        # db.rollback()
        print("Vote Error:", e)
        return HTMLResponse(f"Error while submitting vote: {str(e)}", status_code=500)

