from sqlalchemy.orm import Session
from models.user import User
from schemas.user_schema import UserCreate, UserLogin

def get_users(db: Session):
    return db.query(User).all()

def create_user(db: Session, user: UserCreate):
    user = User(name=user.name, email=user.email, password=user.password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def check_credentials(db: Session, email: str, password: str):
    user_data = None
    user_data = db.query(User).filter(User.email == email).first()
    if(not user_data):
        return None
    if(user_data.password == password):
        return user_data
    else:
        return None
    
def get_user(db: Session, email: str):
    user = db.query(User).filter(User.email == email).first()
    if(user):
        return user
    else:
        return None