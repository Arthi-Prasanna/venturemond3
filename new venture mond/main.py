from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
import os

from database import engine, SessionLocal, Base
import models
import schemas
import auth

# Create Database Tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- Dependencies ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except auth.JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# --- Auth Routes ---

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/register", response_model=schemas.UserBase)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    # Default admin for demo purposes if email contains 'admin'
    role = "admin" if "admin" in user.email.lower() else "client"
    
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    if role == "client":
        client_profile = models.ClientProfile(
            user_id=new_user.id,
            company_name=user.company_name or "New Company",
            project_name=user.project_name or "New Project",
            budget="$0",
            status="Active"
        )
        db.add(client_profile)
        db.commit()

    return new_user

@app.get("/api/users/me", response_model=schemas.UserBase)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# --- Dashboard API Routes ---

@app.get("/api/client/dashboard", response_model=schemas.ClientDashboardSchema)
def get_client_dashboard(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "client":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    profile = current_user.client_profile
    if not profile:
        # Fallback for demo if data missing
        return {
            "project_name": "No Active Project",
            "status": "Inactive",
            "budget": "$0",
            "pending_invoices_count": 0,
            "active_orders_count": 0
        }
    
    return {
        "project_name": profile.project_name,
        "status": profile.status,
        "budget": profile.budget,
        "pending_invoices_count": 0, # Implement real count later
        "active_orders_count": 1
    }

@app.get("/api/admin/clients", response_model=List[schemas.UserBase])
def get_admin_clients(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    clients = db.query(models.User).filter(models.User.role == "client").all()
    return clients

# --- Static Files and Templates ---

# Mount static directory
current_dir = os.path.dirname(os.path.realpath(__file__))
static_dir = os.path.join(current_dir, "static")
templates_dir = os.path.join(current_dir, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
async def read_root():
    return FileResponse(os.path.join(templates_dir, "index.html"))

@app.get("/{filename}")
async def read_html(filename: str):
    # Security: Ensure we don't traverse up
    if ".." in filename or "/" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    if filename.endswith(".html"):
        filename = filename[:-5]
    
    file_path = os.path.join(templates_dir, f"{filename}.html")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
