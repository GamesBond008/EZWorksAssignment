from sqlalchemy import Column, ForeignKey, LargeBinary, String, text
from sqlalchemy.dialects.mysql import ENUM, INTEGER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
	__tablename__ = 'Users'

	id = Column(INTEGER(11), primary_key=True)
	email = Column(String(200), nullable=False)
	userName = Column(String(100), nullable=False)
	password = Column(String(200), nullable=False)
	userType = Column(ENUM('Operation', 'Client'), server_default=text("'Client'"))


class File(Base):
	__tablename__ = 'Files'

	id = Column(INTEGER(11), primary_key=True)
	userId = Column(ForeignKey('Users.id'), nullable=False, index=True)
	file = Column(LargeBinary)
	fileType = Column(String(10), nullable=False)

	User = relationship('User')
