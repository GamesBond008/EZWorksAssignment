from sqlalchemy import Column, ForeignKey, String, text
from sqlalchemy.dialects.mysql import ENUM, INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from app.resources.userTypes import UserTypes

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    id = Column(INTEGER(11), primary_key=True, autoincrement = True)
    email = Column(String(200), nullable=False)
    userName = Column(String(100), nullable=False)
    password = Column(String(200), nullable=False)
    emailVerfied = Column(TINYINT(1), default=0)
    userType = Column(ENUM(UserTypes), default='Client')


class File(Base):
    __tablename__ = 'Files'

    id = Column(INTEGER(11), primary_key=True, autoincrement = True)
    userId = Column(ForeignKey('Users.id'), nullable=False, index=True)
    filePath = Column(String(1000))

    User = relationship('User')
