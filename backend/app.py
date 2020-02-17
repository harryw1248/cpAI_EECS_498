from flask import Flask, render_template, redirect, url_for, request, jsonify
import pyrebase
import pprint
import json

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

def explain_term(content):
   
    # for print debugging
    pprint.pprint(content)

    # map it (in this case, the slot is mapped to the token)
    extract = content['queryResult']['parameters']['terminology']

    tokenized_extract = standardize_token(extract)
    firebase_data = db.child("TERMINOLOGY").get().val()

    with open('response.json') as f:
        data = json.load(f)
        
    if tokenized_extract not in firebase_data:
        data['fulfillment_text'] = "Sorry, I don't think " + extract + " is a relevant tax term"
    else:
        data['fulfillment_text'] = extract + " is "  + firebase_data[tokenized_extract]

    return jsonify(data)

def explain_instructions(content):
    return

def deductions(content):
    return 

def income_and_finances(content):
    return

def refund_and_owe(content):
    return

def third_party_and_sign(content):
    return

def demographics_fill(content):
    return

def welcome(content):
    return

def fallback(content):
    return


    
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get payload
        content = request.json

        # for print debugging
       # pprint.pprint(content)
        intent = content['queryResult']['intent']['displayName']
        print(intent)
        content = request.json
        
        if intent == 'explain_term':
            return explain_term(content)
        elif intent == 'explain_instructions':
            return explain_instructions(content)
        elif intent == 'deductions':
            return deductions(content)
        elif intent == 'income_and_finances':
            return income_and_finances(content)
        elif intent == 'refund_and_owe':
            return refund_and_owe(content)
        elif intent == 'third_party_and_sign':
            third_party_and_sign(content)
        elif intent == 'demographics_fill':
            return demographics_fill(content)
        elif intent == 'Default Welcome Intent':
            return welcome(content)
        else:
            return fallback(content)

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




if __name__ == "__main__":
    app.run(port=5000, debug=True)
