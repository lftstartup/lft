from flask import Flask, render_template, request, redirect, url_for, session as login_session
from werkzeug.utils import secure_filename
import os 
from database import create_student, create_teacher, query_teacher_username, query_student_username, query_teachers, query_students



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

<<<<<<< HEAD
		# #checking if the password contains a number
		# for i in range(len(password)):
		# 	if password[i].isalpha() == False:
		# 		is_numbers = True
		# if is_numbers == False:
		# 	return render_template("register_student.html", msg = "password must contain at least 1 number")

		# #checking if the password contains a letter
		# for i in range(len(password)):
		# 	if password[i].isalpha == True:
		# 		is_letters = True
		# if is_letters == False:
		# 	return render_template("register_student.html", msg = "password must contain at least 1 letter")

		# #checking if the password contains at least 8 characters
		# if len(password) < minimum_characters:
		# 	return render_template("register_student.html", msg = "password must contain at least 8 characters")

		# #checking if the password contains more than 18 characters
		# if len(password) > maximum_characters:
		# 	return render_template("register_student.html", msg = "password is too long, maximum amount of characters allowed is 18")
=======
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
		if len(password) > maximum_characters:
			return render_template("register_student.html", msg = "password is too long, maximum amount of characters allowed is 18")
>>>>>>> 02d48d4a80e3115238bbdfd6866ad3419228b1b9


		create_student(username, password, email)
		login_session['username'] = username
		render_template("home.html", username = login_session['username'])
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
			if password[i].isalpha == True:
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


		create_teacher(firstname, lastname, username, password, credit_num, credit_date, credit_code, email)
		session['username'] = username
		render_template("home.html", username = session['username'])
		return redirect(url_for('home'))



@app.route('/home')
def home():
	return render_template("home.html")


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template("login.html")
	else:
		user = request.form['user']
		if user == "Teacher":
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
						render_template("home.html", username = username)
						return redirect(url_for('home'))


					else:
						is_password = False
					is_username = True
			if is_username == False:
				return render_template("login.html", msg = "the username is not exited in our database :(")
			if is_password == False:
				return render_template("login.html", msg = "the password does not match the username!")

			return render_template("login.html")

if __name__ == '__main__':
    app.run(debug=True)





