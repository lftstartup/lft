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
	email = Column(String)
	language = Column(String)
	courses = Column(Integer)
	buyers = Column(Integer)
	rate_amount = Column(Integer)
	grades = Column(Integer)
	def __repr__(self):
		message = "\nfirst name: " + self.firstname + "\nlast name: " + self.lastname + "\nusername: " + self.username + "\npassword: " + self.password + "\nemail: " + self.email + "\nrating: " + self.rating
#students
class Students(Base):
	__tablename__ = 'students'
	id = Column(Integer, primary_key = True)
	username = Column(String)
	password = Column(String)
	email = Column(String)
	courses = Column(String)
	level = Column(Integer)
	def __repr__(self):
		message = "\nusername: " + self.username + "\npassword: " + self.password + "\nemail: " + self.email + "\n" 
		return "\nstudent id: " + str(self.id) + message
class Quizes(Base):
	__tablename__ = "quizes"
	id = Column(Integer, primary_key = True)
	owner = Column(String)
	language = Column(String)
	subject = Column(String)
	firstquestion = Column(String)
	firstanswer = Column(String)
	secondquestion = Column(String)
	secondanswer = Column(String)
	thirdquestion = Column(String)
	thirdanswer = Column(String)
	def __repr__(self):
		message = "\n\nowner: " + self.owner + "\nlanguage: " + self.language + "\nsubject: " + self.subject + "\nfirst question: " + self.firstquestion + "\nanswer to the first question: " + self.firstanswer + "\nsecond question: " + self.secondquestion + "\nanswer to the second question: " + self.secondanswer + "\nthird question: " + self.thirdquestion + "\nanswer to the third question: " + self.thirdanswer + "\n"
		return message
class Posts(Base):
	__tablename__ = "posts"
	id = Column(Integer, primary_key = True)
	teacher = Column(String)
	title = Column(String)
	content = Column(String)
	video = Column(String)
	def __repr__(self):
		message = "\n\nteacher: " + self.teacher + "\ntitle: " + self.title + "\ncontent: " + self.content + "\nlink for a video: " + self.video
		return message
class Courses(Base):
	__tablename__ = "Courses"
	id = Column(Integer, primary_key = True)
	teacher = Column(String)
	title = Column(String)
	language = Column(String)
	topic = Column(String)
	video_amount = Column(Integer)
	video1 = Column(String)
	video2 = Column(String, nullable = True)
	video3 = Column(String, nullable = True)
	video4 = Column(String, nullable = True)
	video5 = Column(String, nullable = True)
	trailer = Column(String)
	purchased = Column(String)
	buyers = Column(Integer)
	level = Column(Integer)
	def __repr__(self):
		message = "\n\nid: " + str(self.id) + "\nteacher's username: " + self.teacher + "\ntitle: " + self.title + "\nlanguage: " + self.language + "\ntopic: " + self.topic + "\nfirst lecture: " + self.video1 + "\nsecond lecture: " + self.video2 + "\nthird lecture: " + self.video3 + "\nfourth lecture: " + self.video4 + "\nfifth lecture: " + self.video5
		return message
class Advertisers(Base):
	__tablename__ = 'advertisers'
	id = Column(Integer, primary_key = True)
	company_name = Column(String)
	info = Column(String)
	link = Column(String)
	def __repr__(self):
		message = "\ncompany name: " + self.company_name + "\ninfo: " + self.info + "\nlink: " + self.link