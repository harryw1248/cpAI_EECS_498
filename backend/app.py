from flask import Flask, render_template, redirect, url_for, request, jsonify
from document import Document
from user import User
from response import Response
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

intent_to_explainable_term = {}


def unstandardize_token(token):
    return token.replace("_", " ")


def standardize_token(token):
    new_token = token.lower()
    new_token = new_token.replace("-", " ")
    return new_token.replace(" ", "_")


def explain_term_yes(content):
    global last_unfilled_field
    global responses
    global document
    global last_intent
    session = content['session']

    with open('response.json') as f:
        data = json.load(f)

    next_unfilled_slot = document.find_next_unfilled_slot_demographics()
    response = responses.get_next_response(next_unfilled_slot,  document)

    output_context = responses.generate_output_context(last_unfilled_field, 1, session)
    data['fulfillment_messages'] = [{"text": {"text": ["Great, let's move on. " +  response]}}]
    data['output_contexts'] = output_context
    return jsonify(data)



def explain_term(content, extract=None):
    if extract is None:
        extract = content['queryResult']['parameters']['terminology']
    else:
        print(extract)

    tokenized_extract = standardize_token(extract)
    firebase_data = db.child("TERMINOLOGY").get().val()

    with open('response.json') as f:
        data = json.load(f)

    if tokenized_extract not in firebase_data:
        data['fulfillment_messages'] = \
            [{"text": {"text": [
                "Sorry, I don't have a working definition for " + extract + ". Do you want to go back to filling out the form?"]}}]

    else:
        response = "Great question, " + extract + " is " + firebase_data[tokenized_extract] + ". Does that make sense?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    if extract == "filing status":
        global document
        if document.demographic_user_info['is-married']:
            response = "If you file jointly, you and your spouse will fill out one tax form together. If you file separately,"\
                        "each of you will fill out your own tax form. Most of the time, we'll encourage you to file"\
                        "together, but if one of you has significant itemized deductions, it may be better to file together. " \
                       "Later on, we'll let you know if it's better to file separetely. Does that make sense?"
            data['fulfillment_messages'] = [{"text": {"text": [response]}}]
        else:
            response = "If you file had a spouse die within the past two years, you can file as a qualifying widower," \
                       "which brings certain tax deductions.  Does that make sense?"
            data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    global last_intent
    last_intent = 'explain_term'
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


def demographics_fill(content):
    # for print debugging
    parameters = content['queryResult']['parameters']
    global responses
    global user
    global document
    global last_intent
    global last_unfilled_field

    response = None

    current_intent = content['queryResult']['intent']['displayName']

    # Session necessary to generate context identifier
    session = content['session']

    # first pass: update params on document object
    document.update_document_demographics(parameters, current_intent)

    # second pass: query next thing needed
    next_unfilled_slot = document.find_next_unfilled_slot_demographics()

    if next_unfilled_slot is None:
        response = "We're all done filling out your demographics. Let's move on."
        last_intent = 'demographic_fill.dependents'
    elif document.dependent_being_filled is not None:
        print("about to get the next question for dependent")
        response = responses.get_next_dependent_response(
            next_unfilled_slot,
            document.dependent_being_filled.num
        )
    else:
        response = responses.get_next_response(next_unfilled_slot, document)
        print("next_unfilled_slot:" + next_unfilled_slot + " " + response)

    output_context = None
    if next_unfilled_slot is not None:
        output_context = responses.generate_output_context(next_unfilled_slot, 1, session)
        if next_unfilled_slot == 'filing_status' and document.demographic_user_info['filing_status'] == 'single':
            output_context = responses.generate_output_context('dual_status_alien', 1, session)
            next_unfilled_slot = 'dual_status_alien'

    last_unfilled_field = next_unfilled_slot

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = output_context

    global user

    # data[]  # set followup event
    last_intent = 'demographics_fill'
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
    global last_unfilled_field
    global responses
    global document

    if last_unfilled_field == '':
        last_unfilled_field = document.demographics_slots_to_fill[0]
    
    with open('response.json') as f:
        data = json.load(f)

    session = content['session']
    data['fulfillment_messages'] = [{"text": {"text": ["I didn't get that. Can you say it again?"]}}]
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session)

    return jsonify(data)


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
        global last_unfilled_field

        if intent == 'explain_term':
            return explain_term(content)
        elif intent == 'explain_term - yes' or intent == 'explain_previous_term - yes':
            return explain_term_yes(content)
        elif intent == 'explain_previous_term':
            return explain_term(content, unstandardize_token(last_unfilled_field))
        elif intent == 'deductions':
            return deductions(content)
        elif intent == 'income_and_finances':
            return income_and_finances(content)
        elif intent == 'refund_and_owe':
            return refund_and_owe(content)
        elif intent == 'third_party_and_sign':
            third_party_and_sign(content)
        elif intent.startswith('demographics_fill'):
            return demographics_fill(content)
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