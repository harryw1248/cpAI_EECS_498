from flask import Flask, render_template, redirect, url_for, request, jsonify
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

class Document:
    def __init__(self):
        self.demographic_user_info = {'given-name': '',
                         'last-name': '',
                         'location': {
                             'admin-area': '',
                             'business-name': '',
                             'city': '',
                             'country': '',
                             'island': '',
                             'shortcut': '',
                             'street-address': '',
                             'subadmin-area': '',
                             'zip-code': ''
                         },
                         'social_security': '',
                         'filing_status': ''
                         }
        self.demographics_slots_to_fill = ['given-name', 'last-name', 'location', 'social_security', 'filing_status']
        self.ignore_location_info = {'business-name', 'island', 'shortcut', 'subadmin-area', 'country'}
        self.last_unfilled_field = ""

    def check_status(self, slot):
        if slot not in self.demographic_user_info:
            return "Error"
        elif slot == 'location':
            for key, value in self.demographic_user_info['location'].items():
                if value == '' and key not in self.ignore_location_info:
                    return key

            return None
        elif self.demographic_user_info[slot] == '':
            return slot
        else:
            return None

    def find_next_unfilled_slot_demographics(self):
        for slot in self.demographics_slots_to_fill:
            status = self.check_status(slot)
            if status is not None:
                return status

        return None

    def update_document_demographics(self, parameters):
        for slot, value in self.demographic_user_info.items():
            if slot == 'location':
                for location_key, location_value in self.demographic_user_info['location'].items():
                    if location_value == '' and parameters[slot] != '' and parameters[slot][location_key] != '':
                        self.demographic_user_info['location'][location_key] = parameters[slot][location_key]
            elif value == '' and slot in parameters and parameters[slot] != '':
                self.demographic_user_info[slot] = parameters[slot]


class Dependent:
    def __init__(self):
        self.info = {'dependent-name': '', 'dependent-SSN': '', 'dependent-relationship': '',
                     'dependent-child-tax-credit': [[False], False], 'depedent-credit-for-others': [[False], False]}


class User:
    def __init__(self):
        self.demographics = {'given-name': '', 'last-name': '', 'city': '', 'admin-area': '',
                             'street-address': '', 'zip-code': '', 'social_security': '', 'country': '', 'filing_status': -1}
        self.spouse_info = [[False, {'spouse-given-name': '', 'spouse-last-name': '', 'spouse-social_security': '',
                                     'mfs_spouse': ''}], False]

        self.HOH_QW_child = ""
        self.PO = [[False], False]
        self.apt_num = ["", False]
        self.PES = [[False, False], False]
        self.is_foreign_address = [[False, False]]
        self.foreign_country_info = [["", "", ""], False]
        self.more_than_four_dependents = [[False], False]
        self.standard_deduction_checkbox = [[], False]
        self.user_age_blind = [[False, False], False]
        self.spouse_age_blind = [[False, False], False]
        self.list_of_dependents = [[], False]
        self.field_values = dict()

    def jsonify_user(self):
        user_dict = {}
        user_dict['first_name_middle_initial'] = self.demographics['given-name']
        user_dict['last_name'] = self.demographics['last-name']
        user_dict['social_security'] = self.demographics['social_security']
        user_dict['filing_status'] = self.demographics['filing_status']
        user_dict['mfs_spouse'] = self.spouse_info[0][1]['mfs_spouse']
        user_dict['HOH_QW_child'] = self.HOH_QW_child
        user_dict['has_spouse'] = self.spouse_info[0][0]
        user_dict['spouse_first_name_middle_initial'] = self.spouse_info[0][1]['mfs_spouse']
        user_dict['spouse_last_name'] = self.spouse_info[0][1]['spouse-last-name']
        user_dict['spouse_SSN'] = self.spouse_info[0][1]['spouse-social_security']
        user_dict['street-address'] = self.demographics['address']
        user_dict['city'] = self.demographics['city']
        user_dict['state'] = self.demographics['admin-area']
        user_dict['PO'] = self.PO[0][1]
        user_dict['apt_num'] = self.apt_num
        user_dict['PES'] = self.PES
        user_dict['is_foreign_address'] = self.is_foreign_address
        user_dict['foreign_country_info'] = self.foreign_country_info
        user_dict['more_than_four_dependents'] = self.more_than_four_dependents
        user_dict['standard_deduction_checkbox'] = self.standard_deduction_checkbox
        user_dict['user_age_blind'] = self.user_age_blind
        user_dict['spouse_age_blind'] = self.spouse_age_blind
        user_dict['list_of_dependents'] = self.list_of_dependents
        user_dict['field_values'] = self.field_values
        return json.dumps(user_dict)

    def update_demographic_info(self, document):
        for slot in document.demographics_slots_to_fill:
            if slot is not 'location':
                self.demographics[slot] = document.demographic_user_info[slot]
            elif slot == 'location':
                location_vals = document.demographic_user_info['location']
                for inner_slot, inner_slot_val in location_vals.items():
                    if inner_slot in self.demographics:
                        self.demographics[inner_slot] = inner_slot_val


class Response:
    def __init__(self):
        self.demographics = {'given-name': 'What is your given name?',
                        'last-name': 'What is your last name?',
                        'city': 'What city do you live in?',
                        'admin-area': 'What state you live in?',
                        'street-address': 'What is your street address?',
                        'zip-code': 'What is your zip code',
                        'social_security': 'What is your SSN?',
                        'filing_status': 'What is your filing status?'
                        }
        self.demographics_question_order = ['given-name', 'last-name', 'geo-city', 'geo-state', 'address',
                                            'zip-code', 'social_security', 'filing_status']


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
    pprint.pprint(content)
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
    data['output_contexts'] = output_context
    

    global user

    # data[]  # set followup event
    last_intent = 'demographics_fill.self'
    user.update_demographic_info(document)
    return jsonify(data)

def demographics_fill_dependents(content):
    return None

def generate_output_context(slot, lifespan, session):
    global slot_to_output_contexts
    context_identifier = session
    context_identifier = context_identifier + "/contexts/" + slot_to_output_contexts[slot]
    context = [{
        "name": context_identifier,
        "lifespan_count": lifespan
    }]
    return context


def handle_location_parameter(parameters, slot, value):
    global demographic_user_info
    global demographics_slots_to_fill

    for location_key, location_value in demographic_user_info['location'].items():
        # There may be multiple location parameters per utterance
        for location_object in parameters[slot]:
            if location_value == '' and parameters[slot] != '' and location_object[location_key] != '':
                demographic_user_info['location'][location_key] = location_object[location_key]


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
        elif intent.startswith('demographics_fill.self'):
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