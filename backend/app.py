from flask import Flask, render_template, redirect, url_for, request
import pyrebase

config = {
  "apiKey": "AIzaSyBFSeIw9rHMwh59tlEbAM3fcjVPL2ieu70",
  "authDomain": "cpai-bf71c.firebaseapp.com",
  "databaseURL": "https://cpai-bf71c.firebaseio.com",
  "projectId": "cpai-bf71c",
  "storageBucket": "cpai-bf71c.appspot.com",
  "messagingSenderId": "305447636105",
  "appId": "1:305447636105:web:195858d535ea28ffb10a58",
  "measurementId": "G-C71QZDCC4E"
}


app = Flask(__name__)
firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.child("names").push({"name": "Vinny"})

#@app.route('/')
#def create_new_user():
#  print("hello")

#@app.route('/hello')
@app.route('/')
def home():
    return 'Welcome to CPai!'

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/user')
def create_new_user():
    print("Hello")
    return "hello"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
