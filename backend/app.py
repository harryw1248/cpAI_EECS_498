from flask import Flask, render_template, redirect, url_for, request, jsonify
import pyrebase
import pprint

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

#@app.route('/explain_term', methods=['POST'])
def explain_term():
    # get payload
    content = request.json

    # for print debugging
    pprint.pprint(content)

    # map it (in this case, the slot is mapped to the token)
    extract = content['queryResult']['parameters']['terminology']
    extract = standardize_token(extract)
    firebase_data = db.child("TERMINOLOGY").get().val()
    print(content['queryResult']['parameters']['term_definition'])
    if extract not in firebase_data:
        content['queryResult']['parameters']['term_definition'] = "Sorry, I don't think that's a relevant tax term"
    else:
        content['queryResult']['parameters']['term_definition'] = firebase_data[extract]

    return jsonify(content)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get payload
        content = request.json

        # for print debugging
       # pprint.pprint(content)
        intent = content['queryResult']['intent']['displayName']
        print(intent)
        if intent == 'explain_term':
            return explain_term()

    else:
        return "Welcome to CPai!"

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/new_user')
def create_new_user():
    content = request.json

    # for print debugging
    pprint.pprint(content)


    print("Hello")
    return "hello"

def standardize_token(token):
    new_token = token.lower()
    return new_token.replace(" ", "_")




if __name__ == "__main__":
    app.run(port=5000, debug=True)
