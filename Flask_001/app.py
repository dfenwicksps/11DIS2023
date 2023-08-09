# This is a simple login for a Flask app
# A user can login with a username and password
# The username and password are stored in a database using SQLite
# The password is hashed using the werkzeug library
# The user is redirected to the home page if they successfully login
# The user is redirected to the login page if they fail to login
# The user is redirected to the login page if they try to access the home page without logging in

#  Path: Flask_001/app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session  # for Flask
import sqlite3  # for database
from werkzeug.security import generate_password_hash, check_password_hash  # for hashing passwords

app = Flask(__name__)  # create an instance of the Flask class called app
app.secret_key = 's3cr3t'  # set the secret key for the session (used to encrypt session data) - this should be a long random string
# the secret key should be stored in a separate file and imported, CSRF protection should also be enabled
def init_db():  # create the database if it doesn't exist
    with app.app_context():  # app.app_context() pushes an application context, which is required to access current_app
        db = sqlite3.connect('users.db')  # create a connection to the database
        cursor = db.cursor()  # create a cursor object to execute SQL statements
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT UNIQUE, password TEXT)''')  # create a table if it doesn't exist
        db.commit()  # commit the changes

@app.route('/')  # route() decorator binds a function to a URL
def home():  # this function is executed when the user visits the home page
    return render_template('index.html')  # render the index.html template

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        try:
            with sqlite3.connect('users.db') as db:
                cursor = db.cursor()
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
                db.commit()
            flash('Registered successfully!', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists!', 'danger')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect('users.db') as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = cursor.fetchone()
            if user and check_password_hash(user[1], password):
                session['user'] = user[0]
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
# This is a simple login for a Flask app