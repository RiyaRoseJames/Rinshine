# Store this code in 'app.py' file
#from typing_extensions import ParamSpecArgs
from os import name
from firebase import Firebase
from flask import Flask, render_template, request, redirect, url_for, session
#from flask_mysqldb import MySQL
import re
app = Flask(__name__)


config = {
    "apiKey": "AIzaSyDJs8fTB9Q47gdwYKQKOij3fyfqgoN7BlY",
    "authDomain": "rinshine-19bb6.firebaseapp.com",
    "projectId": "rinshine-19bb6",
    "storageBucket": "rinshine-19bb6.appspot.com",
    "messagingSenderId": "415236857970",
    "appId": "1:415236857970:web:8c1b2959c7ce2b597fa2eb",
    "databaseURL": "https://rinshine-19bb6-default-rtdb.firebaseio.com/"
}

firebase = Firebase(config)
# Get a reference to the auth service
auth = firebase.auth()


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        user = auth.sign_in_with_email_and_password(username, password)
        print(user)
        db = firebase.database()
        users1 = db.child("users").get()
        for users in users1.each():
            data = users.key()

        user = {'username': username,
                "event_title": data, 
        }
        return render_template('profile.html', user=user)
        # if account:
        # 	session['loggedin'] = True
        # 	session['id'] = account['id']
        # 	session['username'] = account['username']
        # 	msg = 'Logged in successfully !'
        # 	return render_template('index.html', msg = msg)
        # else:
        # 	msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)

@app.route('/profile/event', methods=['GET', 'POST'])
def event_reg():
    title = request.form['title']
    date = request.form['date']
    time = request.form['time']  
    print(title, date, time) 
    db = firebase.database()
    db.child("users").child(title)
    data = {"Title": title, 
            "Date": date,
            "time" : time,
    }
    db.child("users").push(data) 
    return 'Done'

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        print(auth.create_user_with_email_and_password(email, password))
        msg = 'You have successfully registered !'
        return 'Account created'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route('/home', methods=['GET', 'POST'])
def home():
    msg= ''
    return render_template('home.html', msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
