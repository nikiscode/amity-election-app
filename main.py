from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from routers import auth, vote, admin, profile, nominate, results, elections
import config
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

app = FastAPI()

app.add_middleware(SessionMiddleware, secret_key=config.SECRET_KEY)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(elections.router)
app.include_router(nominate.router)
# app.include_router(users.router)
app.include_router(vote.router)
app.include_router(admin.router)
app.include_router(profile.router)
app.include_router(results.router)

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

    # return {"message": "Welcome to Amity Student Voting System! Visit /auth/login or /auth/register to start."}


# from fastapi import FastAPI, Request, Form, Depends, status
# from fastapi.responses import RedirectResponse
# from fastapi.templating import Jinja2Templates
# from fastapi.staticfiles import StaticFiles

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Dummy user session and admin check (replace with your session system)
# def admin_required(func):
#     async def wrapper(request: Request, *args, **kwargs):
#         user = request.session.get("user") if hasattr(request, 'session') else None
#         if not user or user.get("email") not in ["admin@amity.edu"]:
#             return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
#         return await func(request, *args, **kwargs)
#     return wrapper

# # DB instance placeholder, replace with your actual DB connection object
# database = ...  # Your async DB connection (e.g., databases.Database)

# @app.get("/admin/candidates")
# @admin_required
# async def admin_candidates(request: Request):
#     query = "SELECT * FROM candidates WHERE status='pending'"
#     candidates = await database.fetch_all(query)
#     return templates.TemplateResponse("admin_candidates.html", {"request": request, "candidates": candidates})

# @app.post("/admin/candidates/approve")
# @admin_required
# async def approve_candidate(candidate_id: int = Form(...)):
#     query = "UPDATE candidates SET status='approved' WHERE id = :candidate_id"
#     await database.execute(query, values={"candidate_id": candidate_id})
#     return RedirectResponse("/admin/candidates", status_code=status.HTTP_303_SEE_OTHER)

# @app.post("/admin/candidates/reject")
# @admin_required
# async def reject_candidate(candidate_id: int = Form(...)):
#     query = "DELETE FROM candidates WHERE id = :candidate_id"
#     await database.execute(query, values={"candidate_id": candidate_id})
#     return RedirectResponse("/admin/candidates", status_code=status.HTTP_303_SEE_OTHER)

# @app.get("/results")
# @admin_required
# async def results(request: Request):
#     setting = await database.fetch_one("SELECT value FROM settings WHERE key_name = 'results_visible'")
#     if not setting or setting["value"] != "true":
#         return templates.TemplateResponse("results_not_available.html", {"request": request})

#     candidates = await database.fetch_all("SELECT * FROM candidates WHERE status='approved'")
#     votes_raw = await database.fetch_all("SELECT candidate_id, COUNT(*) as votes FROM votes GROUP BY candidate_id")
#     votes_count = {v["candidate_id"]: v["votes"] for v in votes_raw}

#     return templates.TemplateResponse("results.html", {
#         "request": request,
#         "candidates": candidates,
#         "votes_count": votes_count
#     })
