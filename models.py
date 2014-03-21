from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy import *
import datetime
import md5
from sqlalchemy.dialects.postgresql import BYTEA
from sqlalchemy.orm import relationship, backref
from database import Base
import time



class User(Base):
  __tablename__ = 'register'
  id = Column(Integer, primary_key = True)
  firstname = Column(String(15))
  lastname = Column(String(15))
  phone = Column(String(15), unique=True)
  country_id = Column(String(100))
  email = Column(String(100), unique=True)
  pwdhash = Column(String(20))
  tapes = relationship('Tape', backref='register', lazy='dynamic')
  #wallet = relationship('Wallet', backref="register", lazy='dynamic')
  
  def __init__(self, firstname, lastname, phone, country_id, email, pwdhash):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.phone = phone
    self.country_id = country_id
    self.email = email.lower()
    self.pwdhash = pwdhash.lower()
    
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
      
  def __repr__(self):
    return '<user %r="">' % (self.firstname, self.lastname, self.phone, self.country_id, self.email)
    
    
class Tape(Base):
  __tablename__ = 'tapes'
  uid = Column(Integer, primary_key = True)
  tape_number = Column(Integer(30), unique=True, default='TAPE')
  project_title = Column(String(50))
  content = Column(String(200))
  status = Column(String(20))
  timestamp = Column(DateTime(timezone=True))
  user_id = Column(Integer, ForeignKey('register.id'))
  author = Column(String(50))
  
  def __init__(self, tape_number, project_title, content, status, timestamp=None, user_id=None, author=None):
        self.tape_number = tape_number.title()
        self.project_title = project_title.title()
        self.content = content.title()
        self.status = status.title()
        self.timestamp = datetime.datetime.utcnow()
        self.user_id = user_id
        self.author = author 
        
  
  def __repr__(self):
    return '<Tape %r %r %r %r>' % (self.tape_number, self.project_title, self.content, self.status, self.timestamp)


