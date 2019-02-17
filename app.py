from flask import Flask, render_template, request, redirect, url_for, session as login_session
from werkzeug.utils import secure_filename
import os 
from database import create_student, create_teacher, query_teacher_username, query_student_username, query_teachers, query_students
from database import create_quizes, get_quizes, get_arab_quizes, get_hebrew_quizes, get_quizes_by_owner, query_arab_teachers, query_hebrew_teachers
from database import query_teacher_id

app = Flask(__name__)

app.config['SECRET_KEY'] = 'asdf'

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

		#checking if the username is available
		students = query_students()
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
		email = request.form['email']

		#checking if the username is available
		teachers = query_teachers()
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

		else:
			username = request.form['username']
			password = request.form['password']

			students = query_students()

			is_username = False
			is_password = False

			for student in students:
				if student.username == username:
					is_username = True

					#check password
					if student.password == password:
						is_password = True
						login_session['username'] = username
						render_template("home.html", username = username)
						return redirect(url_for('home'))
			if is_username == False:
				return render_template("login.html", msg = "the username that was inserted does not exist in our database")
			if is_password == False:
				return render_template("login.html", msg = "the password is incorrect!")

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
			quizes = get_quizes_by_owner(teacher.username)
			return render_template("profile.html", ids = ids, teacher = teacher, quizes = quizes, username = username, usertype = usertype)

@app.route('/logout')
def logout():
    login_session.pop('username', None)
    login_session.pop('usertype', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)





