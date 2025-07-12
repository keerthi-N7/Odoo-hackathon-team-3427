from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    name = Column(String)
    avatar_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    skills_offered = Column(String)
    skills_wanted = Column(String)
    is_public = Column(Boolean, default=True)

    swap_requests_sent = relationship(
        "SwapRequest", back_populates="requester", foreign_keys='SwapRequest.requester_id')
    swap_requests_received = relationship(
        "SwapRequest", back_populates="target", foreign_keys='SwapRequest.target_id')

class SwapRequest(Base):
    __tablename__ = "swap_requests"
    id = Column(Integer, primary_key=True, index=True)
    requester_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer, ForeignKey("users.id"))
    skill_offered = Column(String)
    skill_wanted = Column(String)
    status = Column(String, default="pending")
    message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    requester = relationship("User", back_populates="swap_requests_sent", foreign_keys=[requester_id])
    target = relationship("User", back_populates="swap_requests_received", foreign_keys=[target_id])
    feedback = relationship("Feedback", back_populates="swap_request")

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    swap_request_id = Column(Integer, ForeignKey("swap_requests.id"))
    rating = Column(Integer)
    feedback = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    swap_request = relationship("SwapRequest", back_populates="feedback")
