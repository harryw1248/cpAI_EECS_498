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


class Dependent:
    def __init__(self):
        self.full_name = ""
        self.SSN = ""
        self.relationship_to_filer = ""
        self.child_tax_credit = False
        self.credit_for_other_dependents = False

class User:
    def __init__(self):
        self.first_name_last_initial = ""
        self.SSN = ""
        self.filing_status = -1
        self.mfs_spouse = ""
        self.HOH_QW_child = ""
        self.last_name = ""
        self.spouse_first_name_middle_initial = ""
        self.first_name_last_initial = ""
        self.spouse_last_name = ""
        self.spouse_SSN = ""
        self.home_address = ""
        self.PO = False
        self.apt_num = ""
        self.PES = [False, False]
        self.is_foreign_address= False
        self.foreign_country_info= ["", "", ""]
        self.more_than_four_dependents = False
        self.standard_deduction_checkbox = []
        self.user_age_blind = [False, False]
        self.spouse_age_blind = [False, False]
        self.list_of_dependents = []
        self.field_values = dict()


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
    extract = content['queryResult']['parameters']['terminology']

    tokenized_extract = standardize_token(extract)
    firebase_data = db.child("TERMINOLOGY").get().val()

    with open('response.json') as f:
        data = json.load(f)

    if tokenized_extract not in firebase_data:
        data['fulfillment_messages'] = \
            [{"text": {"text": ["Sorry, I don't think " + extract + " is a relevant tax term. Do you have another question?"]}}]

    else:
        response = "Great question, " + extract + " is "  + firebase_data[tokenized_extract] + ". Do you have another question?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

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
    # for print debugging
    pprint.pprint(content)
    extract = content['queryResult']['parameters']['field']

    tokenized_extract = standardize_token(extract)
    firebase_data = db.child("USERS").get().val()

    with open('response.json') as f:
        data = json.load(f)

    if tokenized_extract not in firebase_data:
        db.child("USERS").push({"name":tokenized_extract})
        data['fulfillment_text'] = "Welcome to cpAI, " + extract + "!"
    else:
        data['fulfillment_text'] = "Welcome back, " + extract + "!"

    return jsonify(data)


def welcome(content):
    current_user = User()
    return "Welcome to cpAI!"

def fallback(content):
    return

def send_back_demographic_info():
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
    user = User()
    app.run(port=5000, debug=True)
