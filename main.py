from fastapi import FastAPI, HTTPException, Depends, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta 
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import Session  # Import Session here!
from database import get_db, engine, Base
from models import User
from schemas import UserResponse
import links
import users
import os
from dotenv import load_dotenv

load_dotenv()

# ENV Variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")



Base.metadata.create_all(bind=engine) # Create tables

# To Run on LocalHost( Ninja-LOQ ) to run for AVD
# uvicorn main:app --reload --host 10.0.0.102 --port 8000
app = FastAPI()

app.include_router(users.router)  # Include the user router
app.include_router(links.router)  # Include the link router

@app.get("/")
def read_root():
    return {"message": "Welcome to the Linkstore API"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)  # Default expiration
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta): # New function for refresh token
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=7)  # Longer expiration for refresh token (adjust as needed)
    to_encode["exp"] = expire
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extract data from payload (e.g., user ID)
        user_id = payload.get("sub")  # "sub" is a common claim for user ID
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        return user_id # Or the entire payload if you need more data
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def verify_refresh_token(token: str): # New function to verify refresh token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")




# Authentication endpoint
@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(days=7) # Refresh token expiration
    refresh_token = create_refresh_token(data={"sub": user.id}, expires_delta=refresh_token_expires)

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token} # Include refresh token in response

# Refresh token endpoint (new)
@app.post("/refresh_token")
async def refresh_access_token(refresh_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)): # Use same auth scheme for refresh token
    user_id = verify_refresh_token(refresh_token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.id}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"} # Issue new access token

# Dependency to get the current user (protected endpoints)
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    user_id = verify_access_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# Example protected endpoint
@app.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Authentication Function (replace with your logic)
def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and user.check_password(password): # Assuming you have a check_password method in your User model
        return user
    return None


# @app.get("/login")
# def login(username: str, password: str, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == username).first()
#     # Check if user exists and password matches
#     if not user or user.password != password:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid username or password"
#         )
    
#     return {"message": "Login successful", "user_id": user.id}
