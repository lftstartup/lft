from model import *
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tables.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


#create a teacher
def create_teacher(firstname, lastname, username, password, credit_num, credit_date, credit_code, email, language):
	teacher = Teachers(firstname = firstname, lastname = lastname, username = username, password = password, credit_num = credit_num, credit_date = credit_date, credit_code = credit_code, email = email, language = language)
	session.add(teacher)
	session.commit()


#create a student
def create_student(username, password, email):
	student = Students(username = username, password = password, email = email)
	session.add(student)
	session.commit()


#getting a teacher by username
def query_teacher_username(username):
	teacher = session.query(Teachers).filter_by(username = username).first()
	return teacher

#getting a teacher by id
def query_teacher_id(ids):
	teacher = session.query(Teachers).filter_by(id = ids).first()
	return teacher

#getting a student by username
def query_student_username(username):
	student = session.query(Students).filter_by(username = username).first()
	return student

#getting all teachers
def query_teachers():
	teachers = session.query(Teachers).all()
	return teachers

#getting all teachers who teaches arabic
def query_arab_teachers():
	teachers = session.query(Teachers).filter_by(language = "arabic").all()
	return teachers

#getting all teachers who teaches hebrew
def query_hebrew_teachers():
	teachers = session.query(Teachers).filter_by(language = "hebrew").all()
	return teachers

#getting all students
def query_students():
	students = session.query(Students).all()
	return students

#creating a quiz
def create_quizes(owner, language, subject, question1, question2, question3, answer1, answer2, answer3):
	quiz = Quizes(owner = owner, language = language, subject = subject, firstquestion = question1, firstanswer = answer1, secondquestion = question2, secondanswer = answer2, thirdquestion = question3, thirdanswer = answer3)
	session.add(quiz)
	session.commit()

#get all quizes
def get_quizes():
	quizes = session.query(Quizes).all()
	return quizes

#get all arabic quizes
def get_arab_quizes():
	quizes = session.query(Quizes).filter_by(language = "arabic").all()
	return quizes

#get all hebrew quizes
def get_hebrew_quizes():
	quizes = session.query(Quizes).filter_by(language = "hebrew").all()
	return quizes

#get all quizes by a specific owener
def get_quizes_by_owner(owner):
	quizes = session.query(Quizes).filter_by(owner = owner).all()
	return quizes

print(query_teachers())
print(get_quizes())