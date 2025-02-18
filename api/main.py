from fastapi import FastAPI, HTTPException, Depends, status 
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session  # Import Session here!
from database import get_db, engine, Base
from models import User
import links
import users



Base.metadata.create_all(bind=engine) # Create tables

# To Run on LocalHost( Ninja-LOQ ) to run for AVD
# uvicorn main:app --reload --host 10.0.0.102 --port 8000
app = FastAPI()

app.include_router(users.router)  # Include the user router
app.include_router(links.router)  # Include the link router

@app.get("/")
def read_root():
    return {"message": "Welcome to the Linkstore API"}




@app.get("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    # Check if user exists and password matches
    if not user or user.password != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return {"message": "Login successful", "user_id": user.id}
