from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session as login_session
from werkzeug.utils import secure_filename
import os 
from database import create_student, create_teacher, query_teacher_username, query_student_username, query_teachers, query_students
from database import create_quizes, get_quizes, get_arab_quizes, get_hebrew_quizes, get_quizes_by_owner, query_arab_teachers, query_hebrew_teachers
from database import query_teacher_id, create_post, query_posts, query_posts_teacher, create_course, query_courses, query_courses_teacher
from database import query_course_id, get_amount_buyers_id, update_buyers, update_teacher_buyers, update_teacher_courses
from database import query_teacher_email, query_student_email
from flask_mail import Mail, Message
UPLOAD_FOLDER = 'static/'
ALLOWED_EXTENSIONS = set(['mp4', 'mov', 'avi', 'flv'])
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
				trailer = request.files['trailer']
				video1 = request.files['file1']
				video2 = request.files['file2']
				video3 = request.files['file3']
				video4 = request.files['file4']
				video5 = request.files['file5']
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
				if not video2.filename:
					if video2 and allowed_file(video2.filename):
					 	filename = secure_filename(video2.filename)
						video2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				if not video3.filename:
					if video3 and allowed_file(video3.filename):
					 	filename = secure_filename(video3.filename)
						video3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				if not video4.filename:
					if video4 and allowed_file(video4.filename):
					 	filename = secure_filename(video4.filename)
						video4.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				if not video5.filename:
					if video5 and allowed_file(video5.filename):
					 	filename = secure_filename(video5.filename)
						video5.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
						videos.append(url_for('uploaded_file', filename = filename))
				create_course(username, title, language, topic, videos, trailer)
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
		credit_num = request.form['credit_num']
		credit_date = request.form['credit_date']
		credit_code = request.form['credit_code']
		language = request.form['language']
		#checking if the language is hebrew or arabic
		if language.upper() != "hebrew".upper() and language.upper() != "arabic".upper():
			return render_template("register_teacher.html", msg = "language has to be either 'hebrew' or 'arabic'")
		language = language.lower()
		#checking if the num length is valid
		if len(credit_num) != num_length:
			return render_template("register_teacher.html", msg = "length of the card number is invalid")
		#checking if the code length is valid
		if len(credit_code) != 3:
			return render_template("register_teacher.html", msg = "code only has 3 numbers")
		#checking if there is a letter
		for i in range(3):
			if credit_code[i].isalpha():
				return render_template("register_teacher.html", msg = "code can only contain numbers")
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
		create_teacher(firstname, lastname, username, password, credit_num, credit_date, credit_code, email, language)
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
			if is_username == False:
				return render_template("login.html", msg = "the username is not exited in our database :(")
			if is_password == False:
				return render_template("login.html", msg = "the password does not match the username!")
		if user == 'student':
			username = request.form['username']
			password = request.form['password']
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
@app.route('/profile/<int:ids>')
def profile(ids):
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			teacher = query_teacher_id(ids)
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
			return render_template("profile.html",availabe = message, true = True, ids = ids, acourses = available_courses, courses = courses[::-1], posts = posts, teacher = teacher, quizes = quizes, username = username, usertype = usertype)
		else:
			return redirect(url_for('login'))
	else:
		return redirect(url_for('login'))
@app.route('/profile_name/<string:name>')
def profile_name(name):
	if 'username' in login_session:
		if 'usertype' in login_session:
			username = login_session['username']
			usertype = login_session['usertype']
			teacher = query_teacher_username(name)
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
			return render_template("profile.html", availabe = message, true = True, false = False, acourses = available_courses, courses = courses[::-1], teacher = teacher, posts = posts, quizes = quizes, username = username, usertype = usertype)
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
def courses(ids):
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
				exsists = True
		for teacher in teachers:
			if teacher.email == email:
				user = query_teacher_email(email)
				exsists = True
		if exsists == True:
			msg = Message("your password recovery",
	        	sender='recycledtrash.meet@gmail.com',
	        	recipients=[email])
			msg.body = user.username + ", your password is: "+ user.password
			mail.send(msg)
			return render_template("forgot_password.html", msg = "successfully sent an email")
		else:
			return render_template("forgot_password.html", msg = "email does not exsist!")
@app.route('/logout')
def logout():
	login_session.pop('username', None)
	login_session.pop('usertype', None)
	return redirect(url_for('login'))
if __name__ == '__main__':
	app.run(debug=True)