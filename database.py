from model import *
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///tables.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


#create a teacher
def create_teacher(firstname, lastname, username, password, credit_num, credit_date, credit_code, email):
	teacher = Teachers(firstname = firstname, lastname = lastname, username = username, password = password, credit_num = credit_num, credit_date = credit_date, credit_code = credit_code, email = email)
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

#getting a student by username
def query_student_username(username):
	student = session.query(Students).filter_by(username = username).first()
	return student

#getting all teachers
def query_teachers():
	teachers = session.query(Teachers).all()
	return teachers

#getting all students
def query_students():
	students = session.query(Students).all()
	return students

print(query_teachers())