from model import *
import os
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
engine = create_engine('sqlite:///tables.db?check_same_thread=False')
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
#create a teacher
def create_teacher(firstname, lastname, username, password, email, language):
	teacher = Teachers(firstname = firstname, lastname = lastname, username = username, password = password, email = email, language = language, courses = 0, buyers = 0, rate_amount = 1, grades = 3)
	session.add(teacher)
	session.commit()
#create a student
def create_student(username, password, email):
	student = Students(username = username, password = password, email = email, courses = "", level = "1")
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
#get quiz by id
def get_quiz_id(ids):
	quiz = session.query(Quizes).filter_by(id = ids).first()
	return quiz
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
#create a post
def create_post(teacher, title, content, video):
	post = Posts(teacher = teacher, title = title, content = content, video = video)
	session.add(post)
	session.commit()
#query posts
def query_posts():
	posts = session.query(Posts).all()
	return posts
#query post by teacher
def query_posts_teacher(teacher):
	posts = session.query(Posts).filter_by(teacher = teacher).all()
	return posts
#create a new lecture
def create_course(teacher, title, language, topic, videos, trailer, level):
	if len(videos) == 1:
		course = Courses(teacher = teacher, title = title, language = language, topic = topic, video1 = videos[0],video_amount = 1, buyers = 0, purchased = "", trailer = trailer, level = level)
	elif len(videos) == 2:
		course = Courses(teacher = teacher, title = title, language = language, topic = topic, video1 = videos[0], video2 = videos[1], buyers = 0, video_amount = 2, purchased = "", trailer = trailer, level = level)
	elif len(videos) == 3:
		course = Courses(teacher = teacher, title = title, language = language, topic = topic, video1 = videos[0], video2 = videos[1], buyers = 0, video3 = videos[2],video_amount = 3, purchased = "", trailer = trailer, level = level)
	elif len(videos) == 4:
		course = Courses(teacher = teacher, title = title, language = language, topic = topic, video1 = videos[0], video2 = videos[1], buyers = 0, video3 = videos[2], video4 = videos[3], video_amount = 4, purchased = "", trailer = trailer, level = level)
	else:
		course = Courses(teacher = teacher, title = title, language = language, topic = topic, video1 = videos[0], video2 = videos[-4],  buyers = 0, video3 = videos[-3], video4 = videos[-2], video5 = videos[-1], video_amount = 5, purchased = "", trailer = trailer, level = level)
	session.add(course)
	session.commit()
#get all courses
def query_courses():
	courses = session.query(Courses).all()
	return courses
#get courses by teacher
def query_courses_teacher(teacher):
	courses = session.query(Courses).filter_by(teacher = teacher).all()
	return courses
#get course by id
def query_course_id(ids):
	course = session.query(Courses).filter_by(id = ids).first()
	return course
#updating the amount of people buying a course:
def update_buyers(ids, amount):
	course = query_course_id(ids)
	course.buyers = amount
	session.commit()
#getting the amount of buyers
def get_amount_buyers_id(ids):
	course = query_course_id(ids)
	return course.buyers
#updating teacher buyers
def update_teacher_buyers(username):
	teacher = query_teacher_username(username)
	teacher.buyers += 1
	session.commit()
#update teacher courses
def update_teacher_courses(username):
	teacher = query_teacher_username(username)
	teacher.courses += 1
	session.commit()
#query teacher by email
def query_teacher_email(email):
	teacher = session.query(Teachers).filter_by(email = email).first()
	return teacher
#query student by email
def query_student_email(email):
	student = session.query(Students).filter_by(email = email).first()
#query courses by level
def query_courses_level(level):
	courses = session.query(Courses).filter_by(level = level).all()
	return courses
#add an advertiser
def add_advertiser(company_name, info, link):
	advertiser = Advertisers(company_name = company_name, info = info, link = link)
	session.add(advertiser)
	session.commit()
#get advertisers
def query_advertisers():
	adverts = session.query(Advertisers).all()
	return adverts
#getting rating of a teacher
def get_rating_teacher(username):
	teacher = session.query(Teachers).filter_by(username = username).first()
	return int(teacher.grades / teacher.rate_amount)
#updating a teacher's rating
def update_rating(username, grade):
	teacher = session.query(Teachers).filter_by(username = username).first()
	teacher.grades += grade
	teacher.rate_amount += 1
	session.commit()
#chat########
#query all chats
def all_chats():
	chats = session.query(Chats).all()
	return chats
#query chat
def query_chat(name):
	
	chats = session.query(Chats).filter_by(name = name).first()
	return chats
#creating a chat
def create_chat(name, username, max_people = 8):
	chat = Chats(name = name, usernames = username, max_people = max_people, current_people = 1)
	session.add(chat)
	session.commit()
#sending a message
def send_message(name, username, message):
	now = str(datetime.datetime.now())[0:-7]
	message = Messages(name = name, message = message, sender = username, time = now)
	print(message)
	session.add(message)
	session.commit()
#add user to chat
def add_user_chat(name, username):
	chat = query_chat(name)
	if username in get_chat_users(name):
		pass
	else:
		chat.usernames += "," + username
		chat.current_people += 1
		session.commit()
#remove user from chat
def remove_from_chat(name, username):
	chat = query_chat(name)
	names = chat.usernames
	new_names = []
	names = names.split(',')
	for n in names:
		if n != username:
			new_names.append(n)
	usernames = ""
	for n in new_names:
		username += n + ","
	usernames = username[0:-1]
	chat.usernames = usernames
	chat.current_people -= 1
	session.commit()
#chat users
def get_chat_users(name):
	chat = query_chat(name)
	if chat != 0:
		names = chat.usernames
		flag = False
		for n in names:
			if n == ",":
				flag = True
		if flag:
			names = names.split(',')
		return names
	else:
		return ""
#getting all chat messages
def get_chat_messages(name):
	chat = query_chat(name)
	messages = session.query(Messages).filter_by(name = name).all()
	return messages
#online######
#adding to the session
def add_online(username):
	onlines = get_online()
	flag = False
	for o in onlines:
		if o.username == username:
			flag = True
	if flag != True:
		online = Online(username = username)
		session.add(online)
		session.commit()
#removing online
def remove_online(username):
	session.query(Online).filter_by(username = username).delete()
	session.commit()
#display all online
def get_online():
	online = session.query(Online).all()
	return online

