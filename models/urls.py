from sqlalchemy import Column, Integer, String, ForeignKey
from database import Base
from datetime import datetime

class URL(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True, index=True)
    short_code = Column(String, unique=True, index=True)
    long_url = Column(String)
    clicks = Column(Integer, default=0)
    created_at = Column(String, index=True, default=str(datetime.now()))
    updated_at = Column(String, index=True, default=str(datetime.now()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)