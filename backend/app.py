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
        self.first_name_middle_initial = ""
        self.last_name = ""
        self.SSN = ""
        self.filing_status = -1
        self.mfs_spouse = ""
        self.HOH_QW_child = ""
        self.last_name = ""
        self.spouse_first_name_middle_initial = ""
        self.spouse_last_name = ""
        self.spouse_SSN = ""
        self.home_address = ""
        self.PO = [[False], False]
        self.apt_num = ["", False]
        self.PES = [[False, False], False]
        self.is_foreign_address= [[False, False]]
        self.foreign_country_info= [["", "", ""], False]
        self.more_than_four_dependents = [[False], False]
        self.standard_deduction_checkbox = [[], False]
        self.user_age_blind = [[False, False], False]
        self.spouse_age_blind = [[False, False], False]
        self.list_of_dependents = [[], False]
        self.field_values = dict()
            
    def jsonify_user(self):
        user_dict = {}
        user_dict['first_name_middle_initial'] = self.first_name_middle_initial
        user_dict['last_name'] = self.last_name
        user_dict['SSN'] = self.SSN
        user_dict['filing_status'] = self.filing_status
        user_dict['mfs_spouse'] = self.mfs_spouse
        user_dict['HOH_QW_child'] = self.HOH_QW_child
        user_dict['last_name'] = self.last_name
        user_dict['spouse_first_name_middle_initial'] = self.spouse_first_name_middle_initial
        user_dict['spouse_last_name'] = self.spouse_last_name
        user_dict['spouse_SSN'] = self.spouse_SSN
        user_dict['home_address'] = self.home_address
        user_dict['PO'] = self.PO
        user_dict['apt_num'] = self.apt_num
        user_dict['PES'] = self.PES
        user_dict['is_foreign_address']= self.is_foreign_address
        user_dict['foreign_country_info']= self.foreign_country_info
        user_dict['more_than_four_dependents'] = self.more_than_four_dependents
        user_dict['standard_deduction_checkbox'] = self.standard_deduction_checkbox
        user_dict['user_age_blind'] = self.user_age_blind
        user_dict['spouse_age_blind'] = self.spouse_age_blind
        user_dict['list_of_dependents'] = self.list_of_dependents
        user_dict['field_values'] = self.field_values
        
        return json.dumps(user_dict)

    def find_last_unfilled_field(self):
        return None


user = User()
last_intent = ""
last_unfilled_field = ""
filled_out  = {'given-name': '',
                'last-name': '',
                        'geo-city': '',
                        'geo-state': '',
                        'address': '',
                        'zip-code': '',
                        'social_security': '',
                        # 'date': 'Tell me the date, bitch',
                        # 'blind-status': 'Are you blind, dumbass? I be walking here.',
                        'filing_status': ''
                        }

demo_order = ['given-name', 'last-name', 'geo-city', 'geo-state', 'address', 'zip-code', 'social_security', 'filing_status']

demo_hard_coded_responses = {'given-name': 'What is your given name?',
                        'last-name': 'What is your last name?',
                        'geo-city': 'What city do you live in?',
                        'geo-state': 'What state you live in?',
                        'address': 'What is your street address?',
                        'zip-code': 'What is your zip code',
                        'social_security': 'What is your SSN?',
                        # 'date': 'Tell me the date, bitch',
                        # 'blind-status': 'Are you blind, dumbass? I be walking here.',
                        'filing_status': 'What is your filing status?'
                        }

def standardize_token(token):
    new_token = token.lower()
    return new_token.replace(" ", "_")


def explain_term_yes(content):
    with open('response.json') as f:
        data = json.load(f)

    response = ''

    for key in demo_order:
        if filled_out[key] == '':
            response = demo_hard_coded_responses[key]
            break

    data['fulfillment_messages'] = [{"text": {"text": ["Great, let's move on." +  response]}}]

    return jsonify(data)

def explain_term(content):
    # for print debugging
    pprint.pprint(content)
    extract = content['queryResult']['parameters']['terminology']

    tokenized_extract = standardize_token(extract)
    firebase_data = db.child("TERMINOLOGY").get().val()

    with open('response.json') as f:
        data = json.load(f)

    if tokenized_extract not in firebase_data:
        data['fulfillment_messages'] = \
            [{"text": {"text": ["Sorry, I don't think " + extract + " is a relevant tax term. Do you want to go back to filling out the form?"]}}]

    else:
        response = "Great question, " + extract + " is "  + firebase_data[tokenized_extract] + ". Does that make sense?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    #global last_intent
    #global user
    #global last_unfilled_field

    #data[]   #set followup event


    #last_intent = 'explain_term'
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

def demographics_fill_self(content):
    # for print debugging
    pprint.pprint(content)
    parameters = content['queryResult']['parameters']


    #tokenized_extract = standardize_token(extract)
    #firebase_data = db.child("USERS").get().val()

    response = None
    for key in demo_order:
        if parameters[key] == '':
            response = demo_hard_coded_responses[key]
            break
        else:
            global filled_out
            filled_out[key] = parameters[key]


    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    #global last_intent
    #global user

    #data[]  # set followup event
    #last_intent = 'demographics_fill.self'
    return jsonify(data)


def welcome(content):
    return "Welcome to cpAI!"


def fallback(content):
    return

def push_demographic_info_to_database(content):
    #change User object based on content

    #push to database
    users_ref = db.child('USERS')
    sample_user = User()
    sample_user.first_name = ""
    sample_user.last_name = ""
    sample_user.SSN = ""
    sample_user.filing_status = -1
    sample_user.mfs_spouse = ""
    sample_user.HOH_QW_child = ""
    sample_user.last_name = ""
    sample_user.spouse_first_name_middle_initial = ""
    sample_user.spouse_last_name = ""
    sample_user.spouse_last_name = ""
    sample_user.spouse_SSN = ""
    sample_user.home_address = ""
    sample_user.PO = False
    sample_user.apt_num = ""
    sample_user.PES = [False, False]
    sample_user.is_foreign_address= False
    sample_user.foreign_country_info= ["", "", ""]
    sample_user.more_than_four_dependents = False
    sample_user.standard_deduction_checkbox = []
    sample_user.user_age_blind = [False, False]
    sample_user.spouse_age_blind = [False, False]
    sample_user.list_of_dependents = []
    sample_user.field_values = dict()

    sample_user_json = sample_user.jsonify_user()
    users_ref.set(sample_user_json)
    return

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # get payload
        content = request.json

        intent = content['queryResult']['intent']['displayName']
        print(intent)
        content = request.json
        
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
