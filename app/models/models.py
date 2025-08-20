from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, JSON, text
from sqlalchemy.orm import relationship
from app.core.config import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    answers = relationship("UserAnswer", back_populates="user")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))
    order = Column(Integer, nullable=False)

    questions = relationship("Question", back_populates="unit")


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    content = Column(String(500), nullable=False)
    options = Column(JSON, nullable=False)
    correct_answer = Column(String(255), nullable=False)

    unit = relationship("Unit", back_populates="questions")
    user_answers = relationship("UserAnswer", back_populates="question")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    selected_answer = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False)
    answered_at = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))

    user = relationship("User", back_populates="answers")
    question = relationship("Question", back_populates="user_answers")