from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()


#Teachers
class Teachers(Base):
	__tablename__ = 'teachers'

	id = Column(Integer, primary_key = True)
	firstname = Column(String)
	lastname = Column(String)
	username = Column(String)
	password = Column(String)
	credit_num = Column(String)
	credit_date = Column(String)
	credit_code = Column(String)
	email = Column(String)


	def __repr__(self):
		message = "\nfirst name: " + self.firstname + "\nlast name: " + self.lastname + "\nusername: " + self.username + "\npassword: " + self.password + "\nemail: " + self.email + "\ncredit card details:\ncredit number: " + self.credit_num + "\ncredit date: " + self.credit_date + "\ncredit code: " + self.credit_code
		return message

#students
class Students(Base):
	__tablename__ = 'students'

	id = Column(Integer, primary_key = True)
	username = Column(String)
	password = Column(String)
	email = Column(String)


	def __repr__(self):
		message = "\nusername: " + self.username + "\npassword: " + self.password + "\nemail: " + self.email
		return message


