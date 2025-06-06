from fastapi import APIRouter, Request, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models import User, Candidate, Vote, Election
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy import func

router = APIRouter()


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

@router.get("/results")
def results_page(request: Request, election_id: int = None, db: Session = Depends(get_db)):
    # Fetch all elections to populate dropdown
    all_elections = db.query(Election).order_by(Election.start_time.desc()).all()

    selected_election = None
    candidates = []
    votes_count = {}
    winner = None
    runner_up = None

    if election_id:
        selected_election = db.query(Election).filter(Election.id == election_id).first()
        if selected_election:
            candidates = db.query(Candidate).filter(
                Candidate.election_id == election_id,
                Candidate.status == "approved"
            ).all()

            # Count votes per candidate
            vote_data = db.query(Vote.candidate_id, func.count(Vote.id)).filter(
                Vote.election_id == election_id
            ).group_by(Vote.candidate_id).all()

            votes_count = {cid: count for cid, count in vote_data}

            # Sort candidates by votes descending
            sorted_candidates = sorted(candidates, key=lambda c: votes_count.get(c.id, 0), reverse=True)

            if sorted_candidates:
                winner = sorted_candidates[0]
                runner_up = sorted_candidates[1] if len(sorted_candidates) > 1 else None
                candidates = sorted_candidates
            else:
                candidates = []

    return templates.TemplateResponse("results.html", {
        "request": request,
        "all_elections": all_elections,
        "selected_election_id": election_id,
        "selected_election": selected_election,
        "candidates": candidates,
        "votes_count": votes_count,
        "winner": winner,
        "runner_up": runner_up,
    })
