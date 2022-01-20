from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from datetime import datetime

class Users():
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)


class Todos():
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True)
    title = Column(String(20), nullable=False)
    description = Column(String(255), nullable=False)
    status = Column(Boolean, nullable=False)
    priority = Column(String(20), nullable=False)
    date_added = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'))