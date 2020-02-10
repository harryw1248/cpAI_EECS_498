from flask import Flask
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

@app.route('/')
def hello_world():
    return 'Thanks, !'



if __name__ == "__main__":
    app.run(port=5000, debug=True)
