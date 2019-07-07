from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session as login_session
from werkzeug.utils import secure_filename
import os 
from database import create_student, create_teacher, query_teacher_username, query_student_username, query_teachers, query_students
from database import create_quizes, get_quizes, get_arab_quizes, get_hebrew_quizes, get_quizes_by_owner, query_arab_teachers, query_hebrew_teachers
from database import query_teacher_id, create_post, query_posts, query_posts_teacher, create_course, query_courses, query_courses_teacher
from database import query_course_id, get_amount_buyers_id, update_buyers, update_teacher_buyers, update_teacher_courses
from database import query_teacher_email, query_student_email, query_courses_level, add_advertiser, query_advertisers, get_rating_teacher, update_rating
from database import add_online, remove_online, get_online
from flask_mail import Mail, Message
import random
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['mp4', 'mov', 'avi', 'flv', 'AVI', 'Avi'])
app = Flask(__name__)
app.config.update(dict(
	DEBUG = True,
	MAIL_SERVER = 'smtp.gmail.com',
	MAIL_PORT = 587,
	MAIL_USE_TLS = True,
	MAIL_USE_SSL = False,
	MAIL_USERNAME = 'recycledtrash.meet@gmail.com',
	MAIL_PASSWORD = 'xzaq1234',
))
mail = Mail(app)
app.config['SECRET_KEY'] = 'asdf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@app.route('/feed', methods = ['GET', 'POST'])
def feed():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			if request.method == 'POST':
				file = request.files['file']
				title = request.form['title']
				content = request.form['content']
				if file and allowed_file(file.filename):
					filename = secure_filename(file.filename)
					file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					create_post(username, title, content, url_for('uploaded_file', filename = filename))
			posts = query_posts()
			return render_template("feed.html", username = username, usertype = usertype, teacher = "teacher", student = "student", posts = posts)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/upload_course', methods = ['GET', 'POST'])
def upload_course():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			if request.method == 'POST':
				language = request.form['language']
				title = request.form['title']
				topic = request.form['topic']
				level = request.form['level']
				trailer = request.files['trailer']
				video1 = request.files['file1']
				video2 = request.files['file2']
				video3 = request.files['file3']
				video4 = request.files['file4']
				video5 = request.files['file5']
				for char in level:
					if char.isalpha() == True:
						return render_template("upload_course.html", msg = "level has to be a number between 1-5")
				# if level < 1 or level > 5:
				# 	return render_template("upload_course.html", msg = "level has to be a number between 1-5")
				if language.upper() != "ARABIC" and language.upper() != "HEBREW":
					return render_template("upload_course.html", msg = "language has to be either hebrew or arabic")
				language = language.lower()
				if trailer and allowed_file(trailer.filename):
					filename = secure_filename(trailer.filename)
					trailer.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					trailer = url_for('uploaded_file', filename = filename)
				else:
					return render_template("upload_course.html")
				if video1 and allowed_file(video1.filename):
					filename = secure_filename(video1.filename)
					video1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
					videos = [url_for('uploaded_file', filename = filename)]
				if video2.filename:
					if video2 and allowed_file(video2.filename):
						filename = secure_filename(video2.filename)
						video2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				if video3.filename:
					if video3 and allowed_file(video3.filename):
						filename = secure_filename(video3.filename)
						video3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				if video4.filename:
					if video4 and allowed_file(video4.filename):
						filename = secure_filename(video4.filename)
						video4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				if video5.filename:
					if video5 and allowed_file(video5.filename):
						filename = secure_filename(video5.filename)
						video5.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				create_course(username, title, language, topic, videos, trailer, level)
				update_teacher_courses(username)
			return render_template("upload_course.html")
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/uploads/<filename>')
def uploaded_file(filename):
	return send_from_directory(app.config['UPLOAD_FOLDER'],
							   filename)
#landing page
@app.route('/')
def landing_page():
	return render_template("landing_page.html")
#student register page
@app.route('/register_student', methods = ['GET', 'POST'])
def register_student():
	maximum_characters = 18
	minimum_characters = 8
	is_numbers = False
	is_letters = False
	if request.method == 'GET':
		return render_template('register_student.html')
	else:
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		#checking if the username and email are available
		teachers = query_teachers()
		students = query_students()
		for teacher in teachers:
			if teacher.email == email:
				return render_template("register_student.html", msg = "email is taken")
		for student in students:
			if student.email == email:
				return render_template("register_student.html", msg = "email is taken")
		for student in students:
			if student.username == username:
				return render_template("register_student.html", msg = "username is taken")
		#checking if the password contains a number
		for i in range(len(password)):
			if password[i].isalpha() == False:
				is_numbers = True
		if is_numbers == False:
			return render_template("register_student.html", msg = "password must contain at least 1 number")
		#checking if the password contains a letter
		for i in range(len(password)):
			if password[i].isalpha() == True:
				is_letters = True
		if is_letters == False:
			return render_template("register_student.html", msg = "password must contain at least 1 letter")
		#checking if the password contains at least 8 characters
		if len(password) < minimum_characters:
			return render_template("register_student.html", msg = "password must contain at least 8 characters")
		#checking if the password contains more than 18 characters
		if len(password) >= maximum_characters:
			return render_template("register_student.html", msg = "password is too long, maximum amount of characters allowed is 18")
		#checking if email has a @
		is_at = False
		for i in range(len(email)):
			if email[i] == "@":
				is_at = True
		if is_at == False:
			return render_template("register_student.html", msg = "an email adress must contain an '@' sign")
		#checking if the ending is .com
		is_com = True
		if len(email) >= 6:
			if email[-4:0] != ".com":
				is_com = False
		else:
			return render_template("register_student.html", msg = "email is too short")
		create_student(username, password, email)
		login_session['username'] = username
		login_session['usertype'] = "student"
		msg = Message("thank you for signing up to LFT!",
				sender='recycledtrash.meet@gmail.com',
				recipients=[email])
		msg.body = "hello " + username + ", your signup has been successful.\n best of luck learning a new language,\nLFT team."
		mail.send(msg)
		render_template("home.html", username = login_session['username'], usertype = login_session['usertype'])
		return redirect(url_for('home'))
@app.route('/register_teacher', methods = ['GET', 'POST'])
def register_teacher():
	maximum_characters = 18
	minimum_characters = 8
	is_numbers = False
	is_letters = False
	num_length = 16
	if request.method == 'GET':
		return render_template('register_teacher.html')
	else:
		username = request.form['username']
		password = request.form['password']
		email = request	.form['email']
		#checking if the username is available
		teachers = query_teachers()
		students = query_students()
		for teacher in teachers:
			if teacher.email == email:
				return render_template("register_teacher.html", msg = "email is taken")
		for student in students:
			if student.email == email:
				return render_template("register_teacher.html", msg = "email is taken")
		for teacher in teachers:
			if teacher.username == username:
				return render_template("register_teacher.html", msg = "username is taken")
		#checking if the password contains a number
		for i in range(len(password)):
			if password[i].isalpha() == False:
				is_numbers = True
		if is_numbers == False:
			return render_template("register_teacher.html", msg = "password must contain at least 1 number")
		#checking if the password contains a letter
		for i in range(len(password)):
			if password[i].isalpha() == True:
				is_letters = True
		if is_letters == False:
			return render_template("register_teacher.html", msg = "password must contain at least 1 letter")
		#checking if the password contains at least 8 characters
		if len(password) < minimum_characters:
			return render_template("register_teacher.html", msg = "password must contain at least 8 characters")
		#checking if the password contains more than 18 characters
		if len(password) > maximum_characters:
			return render_template("register_teacher.html", msg = "password is too long, maximum amount of characters allowed is 18")
		firstname = request.form['firstname']
		lastname = request.form['lastname']
		
		language = request.form['language']
		#checking if the language is hebrew or arabic
		if language.upper() != "hebrew".upper() and language.upper() != "arabic".upper():
			return render_template("register_teacher.html", msg = "language has to be either 'hebrew' or 'arabic'")
		language = language.lower()
		
		#checking if email has a @
		is_at = False
		for i in range(len(email)):
			if email[i] == "@":
				is_at = True
		if is_at == False:
			return render_template("register_student.html", msg = "an email adress must contain an '@' sign")
		#checking if the ending is .com
		is_com = True
		if len(email) >= 6:
			if email[-4:0] != ".com":
				is_com = False
		else:
			return render_template("register_teacher.html", msg = "email is too short")
		create_teacher(firstname, lastname, username, password, email, language)
		login_session['username'] = username
		login_session['usertype'] = "teacher"
		msg = Message("thank you for signing up to LFT!",
				sender='recycledtrash.meet@gmail.com',
				recipients=[email])
		msg.body = "hello " + username + ", your signup has been successful.\n best of luck advertising yourself,\nLFT team."
		mail.send(msg)
		render_template("home.html", username = login_session['username'], usertype = login_session['usertype'])
		return redirect(url_for('home'))
@app.route('/home')
def home():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			add_online(username)

			if usertype == "teacher":
				return render_template("home.html", username = username, usertype = usertype, teacher = "teacher")
			else:
				return render_template("home.html", username = username, usertype = usertype, student = "student")				
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		if 'username' in login_session:
			if 'usertype' in login_session:
				return redirect(url_for('logout'))
		return render_template("login.html")
	else:
		user = request.form['user']
		if user == "teacher":
			username = request.form['username']
			password = request.form['password']
			teachers = query_teachers()
			#if the username is in the database
			is_username = False
			is_password = False
			if len(teachers) > 0:
				for teacher in teachers:
					if teacher.username == username:
						teacher_new = query_teacher_username(username)
						if teacher_new.password == password:
							#confirmed
							is_password = True
							login_session['username'] = username
							login_session['usertype'] = "teacher"
							render_template("home.html", username = username, usertype = login_session['usertype'])

							return redirect(url_for('home'))
						else:
							is_password = False
						is_username = True
			else:
				return render_template('login.html', msg = "there are no users in our database")
			if is_username == False:
				return render_template("login.html", msg = "the username is not exited in our database :(")
			if is_password == False:
				return render_template("login.html", msg = "the password does not match the username!")
		if user == 'student':
			username = request.form['username']
			password = request.form['password']
			students = query_students()
			if len(students) == 0:
				return render_template('login.html', msg = "there are no users in our database")
			student = query_student_username(username)
			if student.password == password:
				login_session['username'] = username
				login_session['usertype'] = 'student'
				return redirect(url_for('home'))
			else:
				return render_template("login.html", msg = "password is incorrect")
@app.route('/create_quiz', methods = ['GET', 'POST'])
def create_quiz():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			if usertype == "teacher":
				if request.method == 'GET':
					return render_template("create_quiz.html", username = username, usertype = usertype)
				else:
					owner = username
					language = request.form['language']
					subject = request.form['subject']
					question1 = request.form['firstquestion']
					answer1 = request.form['firstanswer']
					question2 = request.form['secondquestion']
					answer2 = request.form['secondanswer']
					question3 = request.form['thirdquestion']
					answer3 = request.form['thirdanswer']
					language = language.lower()
					create_quizes(owner, language, subject, question1, question2, question3, answer1, answer2, answer3)
					return render_template("home.html", username = username, usertype = usertype, teacher = "teacher")
			else:
				return render_template("home.html", username = username, usertype = usertype)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/all_teachers')
def all_teachers():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			arabic_teachers = query_arab_teachers()
			hebrew_teachers = query_hebrew_teachers()
			return render_template("all_teachers.html", username = username, usertype = usertype, arabic_teachers = arabic_teachers, hebrew_teachers = hebrew_teachers)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/profile/<int:ids>', methods = ['GET', 'POST'])
def profile(ids):
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			teacher = query_teacher_id(ids)
			if usertype == 'student':
				if request.method == 'POST':
					grade = request.form['grade']
					update_rating(teacher.username, grade)
			rating = get_rating_teacher(teacher.username)
			posts = query_posts_teacher(teacher.username)
			courses = query_courses_teacher(teacher.username)
			available_courses = []
			for course in courses:
				names = course.purchased.split(',')
				for name in names:
					if name == username:
						available_courses.append(course)
			quizes = get_quizes_by_owner(teacher.username)
			message = False
			for course in courses:
				names = course.purchased.split(',')
				for name in names:
					if name == username:
						message = True
						break
			return render_template("profile.html", rating = rating, availabe = message, true = True, ids = ids, acourses = available_courses, alen = len(available_courses), clen = len(courses), zero = 0, courses = courses[::-1], posts = posts, teacher = teacher, quizes = quizes, username = username, usertype = usertype)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/profile_name/<string:name>', methods = ['GET','POST'])
def profile_name(name):
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			teacher = query_teacher_username(name)
			if usertype == 'student':
				if request.method == 'POST':
					grade = request.form['grade']
					update_rating(teacher.username, grade)
			rating = get_rating_teacher(teacher.username)
			posts = query_posts_teacher(name)
			courses = query_courses_teacher(name)
			available_courses = []
			for course in courses:
				names = course.purchased.split(',')
				for name in names:
					if name == username:
						available_courses.append(course)
			quizes = get_quizes_by_owner(teacher.username)
			message = False
			for course in courses:
				names = course.purchased.split(',')
				for name in names:
					if name == username:
						message = True
						break
			return render_template("profile.html", availabe = message, rating = rating, true = True, false = False, acourses = available_courses, alen = len(available_courses), clen = len(courses), zero = 0, courses = courses[::-1], teacher = teacher, posts = posts, quizes = quizes, username = username, usertype = usertype)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/purchased/<int:ids>')
def purchased(ids):
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			course = query_course_id(ids)
			names = course.purchased.split(',')
			exsists = False
			for name in names:
				if name == username:
					exsists = True
			if exsists == False:
				update_buyers(ids, len(names))
				update_teacher_buyers(course.teacher)
				teacher = query_teacher_username(course.teacher)
				email = teacher.email
				student = query_student_username(username)
				sender_email = student.email
				course.purchased += ","+username
				if course.level > int(student.level):
					student.level = course.level
				msg = Message(username + " just bought your course " + course.title,
				sender='recycledtrash.meet@gmail.com',
				recipients=[email])
				msg.body = "hello teacher,\n" + username + " has bought a course, email to respond: " + sender_email
				mail.send(msg)
				msg = Message(username + ", you just bought the course " + course.title,
				sender='recycledtrash.meet@gmail.com',
				recipients=[sender_email])
				msg.body = "hello " + username + ", you bought the course "+course.title+", by " + teacher.firstname + " " + teacher.lastname + ".\nemail to contact: " + email
				mail.send(msg)
			return redirect(url_for('home'))
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/courses/<int:ids>')
def courses(is_password):
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			course = query_course_id(ids)
			names = course.purchased.split(',')
			owner = query_teacher_username(course.teacher)
			exsists = False
			for name in names:
				if name == username:
					exsists = True
			if exsists == False:
				return redirect(url_for('home'))
			else:
				return render_template('watch_course.html', course = course, owner = owner)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/support', methods = ['GET', 'POST'])
def support():
	if 'username' in login_session:
		username = login_session['username']
		if request.method == 'GET':
			return redirect(url_for('home'))
		else:
			question = request.form['question']
			email = request.form['email']
			user = query_student_username(username)
			sender_email = user.email
			msg = Message("Your Student needs help!",
				sender='recycledtrash.meet@gmail.com',
				recipients=[email])
			msg.body = "hello teacher,\n" + username + " has sent you a question:\n" + question + "\nemail to respond: " + sender_email
			mail.send(msg)
			return redirect(url_for('home'))
	else:
		return redirect(url_for('login'))
@app.route('/contact_us', methods = ['GET', 'POST'])
def contact_us():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			if request.method == 'POST':
				if usertype == "student":
					student = query_student_username(username)
					email = student.email
				else:
					teacher = query_teacher_username(username)
					email = teacher.email
				title = request.form['title']
				body = request.form['body']
				msg = Message(username + " has reached out",
					sender='recycledtrash.meet@gmail.com',
					recipients=['recycledtrash.meet@gmail.com'])
				msg.body = username + " has reached out.\n"+ title +"\n" + body + "\n" + email
				mail.send(msg)
			return render_template("contact_us.html")
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/forgot_password', methods = ['GET', 'POST'])
def forgot_password():
	if request.method == 'GET':
		return render_template("forgot_password.html", msg = "insert your email")
	else:
		email = request.form['email']
		students = query_students()
		teachers = query_teachers()
		exsists = False
		for student in students:
			if student.email == email:
				user = query_teacher_email(email)
				msg = Message("your password recovery",
		        	sender='recycledtrash.meet@gmail.com',
		        	recipients=[email])
				msg.body = user.username + ", your password is: "+ user.password
				mail.send(msg)
				return render_template("forgot_password.html", msg = "successfully sent an email")
		for teacher in teachers:
			if teacher.email == email:
				user = query_teacher_email(email)
				msg = Message("your password recovery",
		        	sender='recycledtrash.meet@gmail.com',
		        	recipients=[email])
				msg.body = user.username + ", your password is: "+ user.password
				mail.send(msg)
				return render_template("forgot_password.html", msg = "successfully sent an email")

			
		return render_template("forgot_password.html", msg = "email does not exsist!")

@app.route('/my_profile')
def my_profile():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			teacher = 'teacher'
			student = 'student'
			if usertype == 'student':
				user = query_student_username(username)
				courses = query_courses()
				acourses = []
				for course in courses:
					names = course.purchased.split(',')
					for name in names:
						if name == username:
							acourses.append(course)
				leveled_courses = query_courses_level(int(user.level))
				leveled_teachers = []
				if len(leveled_courses) > 0:
					for course in leveled_courses:
						teach = query_teacher_username(course.teacher)
						leveled_teachers.append(teach)
				upleveled_courses = query_courses_level(int(user.level) + 1)
				upleveled_teachers = []
				if len(upleveled_courses) > 0:
					for course in upleveled_courses:
						teach = query_teacher_username(course.teacher)
						upleveled_teachers.append(teach)
				return render_template('my_profile.html', leveled_teachers = leveled_teachers, upleveled_teachers = upleveled_teachers, courses = acourses, user = user, usertype = usertype, student = student, teacher = teacher)
			else:
				user = query_teacher_username(username)
				courses = query_courses_teacher(username)
				posts = query_posts_teacher(username)
				return render_template('my_profile.html', posts = posts, courses = courses, user = user, usertype = usertype, student = student, teacher = teacher)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/advertisers')
def advertisers():
	if 'username' in login_session:
		if 'usertype' in login_session:
			if login_session['usertype'] == "student":
				username = login_session['username']
				advertisers = query_advertisers()
				return render_template('advertisers.html', username = username, advertisers = advertisers)
			else:
				return redirect(url_for('home'))
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/become_advertiser', methods = ['GET', 'POST'])
def become_advertiser():
	if request.method == 'GET':
		return render_template('become_advertiser.html')
	else:
		company_name = request.form['company_name']
		info = request.form['info']
		link = request.form['link']
		add_advertiser(company_name, info, link)
		redirect(url_for('login'))
		return render_template('login.html')
#route for the chats
@app.route('/chat', methods = ['GET', 'POST'])
def chat():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			if usertype == 'teacher':
				return redirect(url_for('home'))
			else:
				if request.method == 'GET':
					return render_template('chat.html')
				else:
					responses1=['How are you?','How old are you?','What is your name?','Where do you study?','How many siblings do you have?','What is favorite food?']
					sender = username
					reciever = 'computer'
					message = request.form['message']
					send_message(sender, reciever, message)
					response = get_response(responses1)
					send_message('computer', username, response)
					responses1.remove(response)

					sended = get_messages_username(username)
					responses = get_responses_username(username)
					chats = []
					if len(sended) > 0:
						for i in range(len(sended)):
							chats.append(sended[i])
							if i <= len(responses):
								chats.append(responses[i])
					redirect(url_for('chat'))
					return render_template("chat.html", username = username, chats = chats, messages = get_messages_username)




@app.route('/chatroom')
def chatroom():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			return render_tamplate('chatroom.html')
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))


@app.route('/chatlist')
def chatlist():
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']

			listi = get_online()
			return render_template("chatlist.html", listi = listi)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/logout')
def logout():
	remove_online(login_session['username'])
	login_session.pop('username', None)
	login_session.pop('usertype', None)
	return redirect(url_for('login'))
if __name__ == '__main__':
	app.run(debug=True)
