from sqlalchemy.orm import Session
from models.urls import URL
from schemas.url_schema import URLCreate
from uuid import uuid4
from utils import generate_uuid_code
PROHIBITED_URLS_LIST = ['login', 'token', 'register', 'check', 'update', 'delete', 'stats']

def get_urls(db: Session, skip: int = 0, limit: int = 100):
    return db.query(URL).offset(skip).limit(limit).all()

def create_url(db: Session, url: URLCreate, user_id: str):

    check_url = db.query(URL).filter(URL.long_url==url.long_url).first()
    if(check_url):
        return None

    short_code = generate_uuid_code()[:6]
    
    if (short_code in PROHIBITED_URLS_LIST):
        return None
    
    check_short_url = db.query(URL).filter(URL.short_code==short_code).first()
    if(check_short_url):
        return None
    
    new_url = URL(id=str(uuid4()), short_code=short_code, long_url=url.long_url, user_id=user_id)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

def get_url_redirect(db: Session, short_code: str):
    requested_url = db.query(URL).filter(URL.short_code == short_code).first()
    if(requested_url==None):
        return None
    requested_url.clicks = requested_url.clicks + 1
    db.commit()
    db.refresh(requested_url)
    return requested_url

def modify_url(db: Session, id: str, new_long_url: str, user_id: str):
    url=None
    url = db.query(URL).filter(URL.id == id).first()
    if(url==None):
        return None
    if(url.user_id != user_id):
        return None
    url.long_url = new_long_url
    db.commit()
    db.refresh(url)
    return url

def get_original_url(db: Session, short_code: str):
    requested_url = db.query(URL).filter(URL.short_code == short_code).first()
    if(requested_url==None):
        return None
    return requested_url.long_url

def delete_url(db: Session, id: str, user_id: str):
    url_to_delete = db.query(URL).filter(URL.id == id).first()
    if(not url_to_delete):
       return None
    if(url_to_delete.user_id != user_id):
        return None
    db.delete(url_to_delete)
    db.commit()
    return url_to_delete

def get_url_stats(db: Session, id: str):
    url = db.query(URL).filter(URL.id == id).first()
    if(not url):
        return None
    return {"clicks": url.clicks}

def get_user_urls(db: Session, user_id: str):
    url_list = db.query(URL).filter(URL.user_id == user_id).all()
    print(url_list)
    if(not url_list):
        return None
    return url_list