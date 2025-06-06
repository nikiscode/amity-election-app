# Amity Student Voting System

This is a FastAPI-based web application for online student elections, styled with Tailwind CSS to match Amity University branding.

## Features

- User registration and login with secure password hashing
- Role-based access control (students and admins)
- Candidate nomination with symbol image and election video upload
- Admin approval/rejection of candidate nominations
- Voting system with one vote per user
- Controlled results display by admin
- Responsive and modern UI/UX styled with Tailwind CSS
- Session-based authentication

## Installation & Setup

1. Clone the repo and navigate to the project directory.
2. Create and activate a Python virtual environment.
3. Install dependencies:


4. Set up MySQL and create the database:
- Run the SQL commands in `schema.sql` to create tables.
5. Configure your MySQL connection details in `main.py` (look for `DATABASE_URL`).
6. Run the application:

7. Access the app at `http://localhost:8000`

## Notes

- The `static` folder contains images and videos for candidates.
- To create an admin, manually update `is_admin` field in the `users` table.
- Session secret keys are hardcoded for demo; update them in production.
- Uploaded files are saved to `static/images` and `static/videos` folders.

## License

MIT License



## Setup Instructions

1. **Clone repo** and navigate to project root.

2. **Create virtual environment** (optional but recommended):


   python3 -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows


Install dependencies:

pip install fastapi uvicorn sqlalchemy pymysql jinja2 bcrypt python-multipart
Setup MySQL database:

Run the schema.sql file in your MySQL server to create the database and tables.

Update DATABASE_URL in config.py to match your MySQL credentials.

Run the application:

uvicorn main:app --reload
Access the app:

Open http://localhost:8000 in your browser.

Admin user:

Add admin emails in config.py under ADMIN_EMAILS. The first user to register with that email becomes admin.

Notes
Uploading candidate symbols/videos requires additional code to handle file uploads.

Voting results are shown only to admins.

Session middleware uses a secret key in config.py.


Truncate Query 

SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE TABLE votes;
TRUNCATE TABLE candidates;
TRUNCATE TABLE elections;

-- Re-enable foreign key checks
SET FOREIGN_KEY_CHECKS = 1;

ALTER TABLE elections AUTO_INCREMENT = 1;
ALTER TABLE candidates AUTO_INCREMENT = 1;
ALTER TABLE votes AUTO_INCREMENT = 1;