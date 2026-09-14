from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from sqlalchemy.orm import Session
from app.core.security import hash_password, verify_password, create_jwt_token
import uuid
from app.db import models
from app.core.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register")
def register(
    username: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.username == username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed = hash_password(password)
    user_id = str(uuid.uuid4())
    user = models.User(id=user_id, username=username, hashed_password=hashed, role="User", full_name=full_name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"msg": "User created"}


@router.post("/login")
def login():
    return {"access_token": "all-access-pass", "token_type": "bearer"}

@router.get("/login", include_in_schema=False)
def login_redirect():
    return RedirectResponse(url="/")

@router.get("/register", response_class=HTMLResponse)
def register_page():
    html = """
    <html><head><title>Register</title></head>
    <body><h2>Register</h2>
    <form method='post' action='/api/auth/register'>
        Username: <input type='text' name='username'/><br/>
        Password: <input type='password' name='password'/><br/>
        Full Name: <input type='text' name='full_name'/><br/>
        Email: <input type='email' name='email'/><br/>
        <input type='submit' value='Register'/>
    </form>
    </body></html>
    """
    return html



