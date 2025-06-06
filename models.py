
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, UniqueConstraint

from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    email = Column(String(150), unique=True, index=True)
    password = Column(String(255))
    is_admin = Column(Boolean, default=False)
    profile_image = Column(String(255))

    candidates = relationship("Candidate", back_populates="user")
    votes = relationship("Vote", back_populates="user")

class Candidate(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    slogan = Column(String(255))
    symbol_image = Column(String(255))
    video = Column(String(255))
    status = Column(String(50), default="pending")
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    election_id = Column(Integer, ForeignKey('elections.id'), nullable=False)


    user = relationship("User", back_populates="candidates")
    votes = relationship("Vote", back_populates="candidate")
    category = relationship("Category", back_populates="candidates")
    election = relationship("Election", back_populates="candidates")
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)  # foreign key column



class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    election_id = Column(Integer, ForeignKey('elections.id'), nullable=False)
    vote_time = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'election_id', name='_user_election_uc'),)

    user = relationship("User", back_populates="votes")
    candidate = relationship("Candidate", back_populates="votes")
    
    
class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    candidates = relationship("Candidate", back_populates="category")
    elections = relationship("Election", back_populates="category")
    
class Election(Base):
    __tablename__ = 'elections'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True)

    category = relationship("Category", back_populates="elections")
    candidates = relationship("Candidate", back_populates="election")



