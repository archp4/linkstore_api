from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
import os
from models import User,Link  # Import your models (User, etc.)
from database import get_db  # Import your database dependency
from schemas import UserResponse, UserCreate, LinkCreate, LinkResponse # Import your schemas

router = APIRouter(prefix="/users", tags=["users"])

# User Endpoints (same as before, but import dependencies and models)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/validate")
def validate_user_data(user: UserCreate, db: Session = Depends(get_db)):
        # Check if email already exists
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
        )
        
        # Check if username already exists
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )    


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).one()
        return user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, user: UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.id == user_id).one()
        for key, value in user.dict().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).one()
        db.delete(user)
        db.commit()
        return None  # Or return a success message
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


# Link Endpoints

@router.post("/{user_id}/links/", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
def create_link(user_id: str, link: LinkCreate, db: Session = Depends(get_db)):
    try:
      user = db.query(User).filter(User.id == user_id).one()
    except NoResultFound:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db_link = Link(**link.dict(), user_id=user_id) # Associate the link with the user
    db.add(db_link)
    db.commit()
    db.refresh(db_link)
    return db_link

@router.get("/{user_id}/links", response_model=List[LinkResponse])
def get_user_links(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == user_id).one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    links = db.query(Link).filter(Link.user_id == user_id).all()
    return links


@router.post("/{user_id}/profile-pic")
async def upload_profile_picture(
    user_id: str,file: UploadFile, db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.id == user_id).one()
            
            # Create a unique filename
        file_extension = file.filename.split(".")[-1]
        filename = f"user_{user_id}_profile.{file_extension}"
        file_path = f"static/profile_pics/{filename}"
            
            # Ensure directory exists
        os.makedirs("static/profile_pics", exist_ok=True)
            
            # Save the file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
            
            # Update user's profile picture path in database
        user.profile_picture = file_path
        db.commit()
            
        return {"image_path": file_path}
            
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")