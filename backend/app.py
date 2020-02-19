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
demographics_slots_to_fill = [
    'given-name',
    'last-name',
    'location',
    'social_security',
    'filing_status',
    'dual_status_alien',
    'blind']

bool_statuses = [
    'dual_status_alien',
    'blind'
]
    

demographic_user_info  = {'given-name': '',
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
                'filing_status': '',
                'blind': '',
                'dual_status_alien': '',
            }

ignore_location_info = {'business-name', 'island', 'shortcut', 'subadmin-area', 'country'}

demo_hard_coded_responses = {'given-name': 'What is your given name?',
                        'last-name': 'What is your last name?',
                        'location': 'So, where do you currently stay?',
                        'social_security': 'What is your SSN?',
                        'filing_status': 'What is your filing status?',
                        'admin-area': 'Can I have your city, state, and zip code?',
                        'city': 'Can I have your city, state, and zip code?',
                        'street-address': 'Whats your street address?',
                        'zip-code': 'Can I have your city, state, and zip code?',
                        'dual_status_alien': "Are you a dual-status alien?",
                        'blind': "Are you blind?"
                        }

slot_to_output_contexts = {
    'given-name': 'prompt_name',
    'last-name': 'prompt_name',
    'location': 'prompt_address',
    'admin-area': 'prompt_address',
    'city': 'prompt_address',
    'street-address': 'prompt_address',
    'zip-code': 'prompt_address',
    'social_security': 'prompt_social_security',
    'filing_status': 'prompt_filing_status',
    'blind': 'prompt_blind',
    'dual_status_alien': "prompt_dual_status_alien"
}

def check_status(slot):
    global demographic_user_info
    global ignore_location_info

    if slot not in demographic_user_info:
        return "ERROR"
    else:
        if slot == 'location':
            for key, value in demographic_user_info[slot].items():
                if value == '' and key not in ignore_location_info:
                    return key

            return True
        else:
            if demographic_user_info[slot] == '':
                return slot
            else:
                return True

def standardize_token(token):
    new_token = token.lower()
    return new_token.replace(" ", "_")

def explain_term_yes(content):
    global last_unfilled_field
    session = content['session']

    with open('response.json') as f:
        data = json.load(f)

    response = ''

    for slot in demographics_slots_to_fill:
        status = check_status(slot)
        if status != True:
            response = demo_hard_coded_responses[status]
            break

    output_context = generate_output_context(last_unfilled_field, 1, session)
    data['fulfillment_messages'] = [{"text": {"text": ["Great, let's move on. " +  response]}}]
    data['output_contexts'] = output_context

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
    pprint.pprint(parameters)

    # Session necessary to generate context identifier
    session = content['session']

    intent = content['queryResult']['intent']['displayName']

    #tokenized_extract = standardize_token(extract)
    #firebase_data = db.child("USERS").get().val()

    response = None
    global demographic_user_info
    global demographics_slots_to_fill
    global last_unfilled_field

    # pprint.pprint(demographic_user_info)

    # First pass: update params on local user
    for slot, value in demographic_user_info.items():
        if 'location' in parameters and slot == 'location':
            handle_location_parameter(parameters, slot, value)
        # if 'given-name' in parameters and slot == 'given-name':
        #     pass
        # if 'last-name' in parameters and slot == 'last-name':
        #     pass
        # if 'social_security' in parameters and slot == 'social_security':
        #     pass
        # if 'filing_status' in parameters and slot == 'filing_status':
        #     pass
        else:
            if value == '' and slot in parameters and parameters[slot] != '':
                demographic_user_info[slot] = parameters[slot]

    # Check the yes/no answer slots
    global bool_statuses
    for status in bool_statuses:
        if status in intent:
            demographic_user_info[status] = True if 'yes' in intent else False


    # pprint.pprint(demographic_user_info)

    #second pass: query next thing needed
    next_query = ''
    for slot in demographics_slots_to_fill:
        status = check_status(slot)
        if status != True:
            response = demo_hard_coded_responses[status]
            next_query = slot
            break

    last_unfilled_field = next_query

    # Generate the appropriate output context for the next query
    output_context = None
    if next_query != '':
        output_context = generate_output_context(next_query, 1, session)

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = output_context
    

    #global last_intent
    #global user

    #data[]  # set followup event
    #last_intent = 'demographics_fill.self'
    return jsonify(data)


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

    #global last_intent
    #global user

    #data[]  # set followup event
    #last_intent = 'demographics_fill.self'
    return jsonify(data)


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
        elif intent.startswith('demographics_fill.self'):
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
