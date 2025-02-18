from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from models import Link  
from api.database import get_db  
from schemas import LinkCreate, LinkResponse 

router = APIRouter(prefix="/links", tags=["links"])

@router.get("/{link_id}", response_model=LinkResponse)
def get_link(link_id: str, db: Session = Depends(get_db)):
    try:
        link = db.query(Link).filter(Link.id == link_id).one()
        return link
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

@router.put("/{link_id}", response_model=LinkResponse)
def update_link(link_id: str, link: LinkCreate, db: Session = Depends(get_db)):
    try:
        db_link = db.query(Link).filter(Link.id == link_id).one()
        for key, value in link.dict().items():
            setattr(db_link, key, value)
        db.commit()
        db.refresh(db_link)
        return db_link
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")

@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(link_id: str, db: Session = Depends(get_db)):
    try:
        link = db.query(Link).filter(Link.id == link_id).one()
        db.delete(link)
        db.commit()
        return None
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Link not found")