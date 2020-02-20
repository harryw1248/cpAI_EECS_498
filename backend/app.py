from flask import Flask, render_template, redirect, url_for, request, jsonify
from backend_classes import Document, Dependent, User, Response
import pyrebase
import pprint
import json
import copy

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

user = User()
document = Document()
responses = Response()
last_intent = ""
last_unfilled_field = ""


def standardize_token(token):
    new_token = token.lower()
    return new_token.replace(" ", "_")


def explain_term_yes(content):
    global responses
    global document
    global last_intent

    with open('response.json') as f:
        data = json.load(f)

    if "demographics" in last_intent:
        for slot in document.demographics_slots_to_fill:
            status = document.check_status(slot)
            if status is not None:
                data['fulfillment_messages'] = [{"text": {"text": ["Great, let's move on. " +
                                                                   responses.demographics[status]]}}]
                return jsonify(data)
    else:
        data['fulfillment_messages'] = [{"text": {"text": ["Great, let's move on to actually doing the math! "]}}]
        return jsonify(data)


def clear():
    global user
    global document

    dummy_user = User()
    user = copy.deepcopy(dummy_user)
    dummy_document = Document()
    document = copy.deepcopy(dummy_document)

    with open('response.json') as f:
        data = json.load(f)

    return jsonify(data)


def explain_term(content):
    # for print debugging
    # pprint.pprint(content)
    extract = content['queryResult']['parameters']['terminology']

    tokenized_extract = standardize_token(extract)
    firebase_data = db.child("TERMINOLOGY").get().val()

    with open('response.json') as f:
        data = json.load(f)

    if tokenized_extract not in firebase_data:
        data['fulfillment_messages'] = \
            [{"text": {"text": [
                "Sorry, I don't think " + extract + " is a relevant tax term. Do you want to go back to filling out the form?"]}}]

    else:
        response = "Great question, " + extract + " is " + firebase_data[tokenized_extract] + ". Does that make sense?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    return jsonify(data)


def demographics_fill_self(content):
    # for print debugging
    # pprint.pprint(content)
    parameters = content['queryResult']['parameters']
    global responses
    global user
    global document
    global last_intent

    response = None

    # first pass: update params on document object
    document.update_document_demographics(parameters)

    # second pass: query next thing needed
    next_unfilled_slot = document.find_next_unfilled_slot_demographics()

    if next_unfilled_slot is None:
        response = "We're all done filling out your demographics. Let's move on."
        last_intent = 'demographic_fill.dependents'
    else:
        response = responses.demographics[next_unfilled_slot]

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    global user

    # data[]  # set followup event
    last_intent = 'demographics_fill.self'
    user.update_demographic_info(document)
    return jsonify(data)

def demographics_fill_dependents(content):
    return None

def welcome(content):
    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": ["Hello!"]}}]


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


def fallback(content):
    return


def push_demographic_info_to_database(content):
    # change User object based on content

    # push to database
    users_ref = db.child('USERS')
    global user

    user_json = user.jsonify_user()
    users_ref.set(user_json)
    return


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get payload
        content = request.json

        intent = content['queryResult']['intent']['displayName']

        if intent == 'explain_term':
            return explain_term(content)
        elif intent == 'explain_term - yes':
            return explain_term_yes(content)
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
        elif intent == 'demographics_fill.self':
            return demographics_fill_self(content)
        elif intent == 'demographics_fill.dependents':
            return demographics_fill_dependents(content)
        elif intent == 'Default Welcome Intent':
            return welcome(content)
        elif intent == 'goodbye':
            return clear()
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