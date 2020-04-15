from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response, send_file
from document import Document
from user import User
from response import Response
import pyrebase
import pprint
import json
import copy
import pdf

config = {
    "apiKey": "AeIzaSyBFSeIw9rHMwh59tlEbAM3fcjVPL2ieu70",
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
last_term_explained = ""
last_field_changed = ""
last_output_context = ""

intent_to_explainable_term = {}
missed_deduction_values = []
previous_deduction_result = None


def unstandardize_token(token):
    return token.replace("_", " ")


def standardize_token(token):
    new_token = token.lower()
    new_token = new_token.replace("-", " ")
    return new_token.replace(" ", "_")


def explain_term_yes(content):
    """Handle conversation logic when the user understands the explanation given from explain_term."""

    global last_unfilled_field
    global responses
    global document
    global last_output_context
    session = content['session']

    with open('response.json') as f:
        data = json.load(f)

    next_unfilled_slot = document.find_next_unfilled_slot()
    print("SUDSDSDDSDSDSDS", next_unfilled_slot)

    if last_unfilled_field == "":
        response = "First we need to gather some basic demographic information. Tell me your name, age, and occupation."
        output_context = responses.generate_output_context("given-name", 1, session, document)
    elif 'deduction' in last_unfilled_field and document.deduction_stage != 'user_done':
        response = "What other deductions you want to claim? If you want help from us, just say so!"
        output_context = responses.generate_output_context('deduction-success', 1, session, document)
    else:
        response = responses.get_next_response(next_unfilled_slot, document)
        output_context = responses.generate_output_context(last_unfilled_field, 1, session, document)

    data['fulfillment_messages'] = [{"text": {"text": ["Great, let's move on. " + response]}}]
    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    return jsonify(data)


def explain_term_repeat(content):
    """Handle logic for when the user did not understand the explanation from explain_term."""
    global last_unfilled_field
    global responses
    global document
    global last_intent
    global last_term_explained
    session = content['session']

    with open('response.json') as f:
        data = json.load(f)

    firebase_data = db.child("TERMINOLOGY").get().val()

    next_unfilled_slot = document.find_next_unfilled_slot()

    if last_unfilled_field == "":
        response = "First we need to gather some basic demographic information. Tell me your name, age, and occupation."
        output_context = responses.generate_output_context("given-name", 1, session, document)
    else:
        response = responses.get_next_response(next_unfilled_slot, document)
        output_context = responses.generate_output_context(last_unfilled_field, 1, session, document)

    data['fulfillment_messages'] = [
        {
            "text": {
                "text": [
                    "I am sorry to hear that. Here is a link that should provide you with some more details:"
                ]
            }
        },
        {
            "card": {
                "buttons": [
                    {
                        "text": firebase_data[last_term_explained]["link"],
                        "postback": firebase_data[last_term_explained]["link"]
                    }
                ]
            }
        },
        {
            "text": {
                "text": [
                    "Whenever you are ready, let's continue. " + response
                ]
            }
        }, ]

    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    return jsonify(data)


def explain_term(content, extract=None):
    global last_term_explained

    if extract is None:
        extract = content['queryResult']['parameters']['terminology']
    else:
        print(extract)

    tokenized_extract = standardize_token(extract)
    last_term_explained = tokenized_extract
    firebase_data = db.child("TERMINOLOGY").get().val()

    with open('response.json') as f:
        data = json.load(f)

    if tokenized_extract not in firebase_data:
        data['fulfillment_messages'] = \
            [{"text": {"text": [
                "Sorry, I don't have a working definition for " + extract + ". Do you want to go back to filling out the form?"]}}]

    else:
        print(firebase_data[tokenized_extract]["definition"])
        print(extract)
        print(tokenized_extract)
        response = "Great question, " + extract + " is " + firebase_data[tokenized_extract][
            "definition"] + ". Does that make sense?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    if extract == "filing status":
        global document
        if document.demographic_user_info['is-married']:
            response = "If you file jointly, you and your spouse will fill out one tax form together. If you file separately, " \
                       "each of you will fill out your own tax form. Most of the time, we'll encourage you to file " \
                       "together, but if one of you has significant itemized deductions, it may be better to file together. " \
                       "Later on, we'll let you know if it's better to file separetely. Does that make sense?"
            data['fulfillment_messages'] = [{"text": {"text": [response]}}]
        else:
            response = "If you file had a spouse die within the past two years, you can file as a qualifying widower," \
                       "which brings certain tax deductions.  Does that make sense?"
            data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    elif 'deduction' in extract:
        response = "A deduction is essentially a discount on your taxes that you get by performing actions that " \
                   "the government sees as bettering society overall. Does that make sense?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    global last_intent
    last_intent = 'explain_term'
    return jsonify(data)


def clear():
    global user
    global document
    global responses
    global last_output_context
    global last_intent
    global last_unfilled_field
    global missed_deduction_values

    dummy_user = User()
    user = copy.deepcopy(dummy_user)
    dummy_document = Document()
    document = copy.deepcopy(dummy_document)
    dummy_responses = Response()
    responses = copy.deepcopy(dummy_responses)

    last_output_context = ""
    last_unfilled_field = ""
    last_intent = "goodbye"

    missed_deduction_values = []

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": ["Great, thank you for using CPai!"]}}]
    print(data)
    return jsonify(data)


def error_checking(parameters, intent, last_unfilled, queryText=None):
    global document

    # possible_error_intents = ['address', 'social_security', 'spouse_SSN', 'money-negative']
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    requires_money_values = ['wages', 'tax-exempt-interest', 'taxable-interest', 'pensions-and-annuities',
                             'pensions-and-annuities-taxable', 'qualified-dividends', 'ordinary-dividends',
                             'IRA-distributions',
                             'IRA-distributions-taxable', 'capital-gains', 'taxable-refunds', 'business-income',
                             'unemployment-compensation',
                             'other-income', 'total-other-income', 'total-income', 'educator-expenses',
                             'business-expenses',
                             'health-savings-deductions', 'moving-expenses-armed-forces',
                             'self-employed-health-insurance',
                             'IRA-deductions', 'tuition-fees', 'adjustments-to-income', 'adjusted-gross-income',
                             'federal-income-tax-withheld',
                             'earned-income-credit', 'ss-benefits', 'ss-benefits-taxable', 'business-gains', '11a',
                             'taxable-income']

    if 'address' in intent:
        value = str(parameters['zip-code'])
        if len(value) != 5:
            return 'street_address', 'You entered an invalid ZIP code. A valid ZIP code consists of five numbers. '
        for digit in value:
            if digit not in digits:
                return 'street_address', 'You entered an invalid ZIP code. A valid ZIP code consists of five numbers. '

    elif 'social_security' in intent:
        value = str(parameters['social_security'])
        num_digits = 0
        num_hyphens = 0

        if value[0] == '-':
            return 'social_security', 'You entered an invalid SSN. Valid SSNs cannot be negative. '

        for digit in value:
            if digit in digits:
                num_digits += 1

                if num_digits > 9:
                    return 'social_security', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

            elif digit == '-':
                num_hyphens += 1
            else:
                return 'social_security', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

        if num_digits != 9:
            return 'social_security', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

    elif 'spouse_SSN' in intent:
        value = str(parameters['spouse-ssn'])
        num_digits = 0
        num_hyphens = 0

        if value[0] == '-':
            return 'social_security', 'You entered an invalid SSN. Valid SSNs cannot be negative. '

        for digit in value:
            if digit in digits:
                num_digits += 1

                if num_digits > 9:
                    return 'spouse-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

            elif digit == '-':
                num_hyphens += 1
            else:
                return 'spouse-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

        if num_digits != 9:
            return 'spouse-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '
    
    elif 'dependent_ssn' in intent:
        value = str(parameters['dependent-ssn'])
        num_digits = 0
        num_hyphens = 0

        if value[0] == '-':
            return 'social_security', 'You entered an invalid SSN. Valid SSNs cannot be negative. '

        for digit in value:
            if digit in digits:
                num_digits += 1

                if num_digits > 9:
                    print("Too many digits")
                    return 'dependent-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

            elif digit == '-':
                num_hyphens += 1
            else:
                print(value)
                print("Invalid character: " + str(digit))
                return 'dependent-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

        if num_digits != 9:
            print("Too many digits")

            return 'dependent-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

    elif intent == 'income_and_finances_fill.monetary_value':
        dollar_value = str(parameters['value'])
        dollar_value_2 = ''
        if parameters['dollar'] != '':
            dollar_value_2 = str(parameters['dollar']["amount"])
        if '-' in dollar_value or '-' in dollar_value_2:
            return last_unfilled, 'You entered a negative dollar amount. Only non-negative values are allowed. '

        try:
            float(dollar_value)
            # float(dollar_value_2)
        except ValueError:
            try:
                float(dollar_value_2)
            except ValueError:
                return last_unfilled, 'You entered an invalid dollar amount. Non-numeric characters are not allowed. '

    elif intent == 'income_and_finances_fill.monetary_value_list':
        dollar_value = str(parameters['value'])
        for value in parameters['value']:
            dollar_value = str(value)
            if '-' in dollar_value:
                return last_unfilled, 'You entered a negative dollar amount. Only non-negative values are allowed. '

            try:
                float(dollar_value)
            except ValueError:
                return last_unfilled, 'You entered an invalid dollar amount. Non-numeric characters are not allowed. '

        for value in parameters['dollar']:
            dollar_value = str(value["amount"])
            print(dollar_value)
            if '-' in dollar_value:
                return last_unfilled, 'You entered a negative dollar amount. Only non-negative values are allowed. '

            try:
                float(dollar_value)
            except ValueError:
                return last_unfilled, 'You entered an invalid dollar amount. Non-numeric characters are not allowed. '

    if intent == 'refund_and_owe.number_value' and last_unfilled == 'routing-number':
        if len(str(parameters['number'])) != 11:
            return last_unfilled, 'You entered an invalid routing number. Please type in exactly 9 digits for your routing number.'
    elif intent == 'refund_and_owe.number_value' and last_unfilled == 'account-number':
        num = str(parameters['number'])
        if not num.endswith('e+16'):
            return last_unfilled, 'You entered an invalid account number. Please type in exactly 17 digits for your routing number.'
    elif intent == 'refund_and_owe.number_value' and (
            last_unfilled == 'overpaid-applied-tax' or last_unfilled == 'amount-refunded'):
        if type(parameters['number']) != str and (parameters['number'] > document.refund_user_info["overpaid"]):
            return last_unfilled, 'You cannot use an amount greater than the amount you overpaid. Please give a\
                 number equal to or less than ${}.'.format(document.refund_user_info["overpaid"])

    if intent == 'third_party.phone_number':
        if len(str(parameters['phone-number'])) != 10:
            return last_unfilled, 'You entered an invalid phone number. Please type in exactly 10 digits.'
    elif intent == 'third_party.pin':
        if len(str(parameters['PIN'])) != 7:
            return last_unfilled, 'You entered an invalid PIN. Please type in exactly 5 digits.'

    if intent == 'demographics_fill.email_phone_number':
        email = str(parameters['email'])
        phone_number = str(parameters["user-phone-number"])

        if email != '' and '@' not in email:
            return 'email', 'You entered an invalid email.'
        
        if phone_number != '' and len(phone_number) != 10:
            return 'user-phone-number', 'You entered an invalid phone number. Please type in exactly 10 digits.'

    return None, None


def demographics_fill(content):
    # for print debugging
    parameters = content['queryResult']['parameters']
    queryText = content['queryResult']['queryText']
    global responses
    global user
    global document
    global last_intent
    global last_unfilled_field

    response = None

    current_intent = content['queryResult']['intent']['displayName']

    # Session necessary to generate context identifier
    session = content['session']

    # Check for valid input
    error_field, error_message = error_checking(parameters, current_intent, last_unfilled_field, queryText)
    
    # No error, update information and get new slot to query from user
    if error_field is None and error_message is None:
        # first pass: update params on document object
        document.update_slot(parameters, current_intent, last_unfilled_field)

        # second pass: query next thing needed
        next_unfilled_slot = document.find_next_unfilled_slot()
    else:
        next_unfilled_slot = error_field
    last_unfilled_field = next_unfilled_slot

    # Must handle dependents separately since they are their own class
    if document.dependent_being_filled is not None:
        response = responses.get_next_dependent_response(next_unfilled_slot, document.dependent_being_filled.num,
                                                         document.dependents)
        if error_field == 'dependent-ssn':
            response = error_message + response

    # Next slot is a demographic slot, get the appropriate response
    elif next_unfilled_slot in document.demographic_user_info or next_unfilled_slot in document.demographic_spouse_info:
        response = responses.get_next_response(next_unfilled_slot, document)
        if error_message is not None:
            response = error_message + response

    # No more slots remaining to fill, proceed to next section of form
    else:
        response = "We're all done filling out your demographics. Let's move onto your income section! "
        if len(document.dependents) > 0:
            name = document.dependents[-1].slots['dependent-given-name']
            if document.dependents[-1].dependent_child_tax_credit:
                addition = name + " qualifies for a child tax credit. "
            elif document.dependents[-1].dependent_credit_for_others:
                addition = name + " qualifies for a dependent credit for others. "
            else:
                addition = name + " unfortunately does not qualify for a tax credit. "

            response = addition + response

    # Set output contexts so that the next utterance can only match with the intents what we're asking about
    output_context = None
    if (next_unfilled_slot in document.demographic_user_info
            or next_unfilled_slot in document.demographic_spouse_info
            or document.dependent_being_filled is not None):
        output_context = responses.generate_output_context(next_unfilled_slot, 1, session, document)
    else:
        response += responses.income_finances['wages']
        output_context = responses.generate_output_context('wages', 1, session, document)
        document.current_section_index += 1
        next_unfilled_slot = 'wages'

    last_unfilled_field = next_unfilled_slot
    print("inside demographics_fill, last_unfilled field is", last_unfilled_field)

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    print("output_context:", output_context)
    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    global user

    last_intent = 'demographics_fill'
    user.update_demographic_info(document)
    return jsonify(data)


def income_finances_fill(content):
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
    error_field, error_message = error_checking(parameters, current_intent, last_unfilled_field)

    if error_field is None and error_message is None:
        document.update_slot(parameters, current_intent, last_unfilled_field)

        # second pass: query next thing needed
        next_unfilled_slot = document.find_next_unfilled_slot()
    else:
        next_unfilled_slot = error_field
    print("next_unfilled_slot: " + str(next_unfilled_slot))

    if next_unfilled_slot is None:
        response = "We're all done filling out your income and finances. Let's move onto calculating your deductions! "
        last_intent = 'income_and_finances_fill.social_security_benefits'
    else:
        response = responses.get_next_response(next_unfilled_slot, document)
        if error_message is not None:
            response = error_message + response

    output_context = None

    # Set output contexts so that the next utterance can only match with the intents what we're asking about
    if (next_unfilled_slot in document.income_user_info):
        output_context = responses.generate_output_context(next_unfilled_slot, 1, session, document)
    else:
        output_context = responses.generate_output_context('deduction-begin', 1, session, document)
        response += responses.deductions['deduction-begin']
        next_unfilled_slot = 'deduction-begin'
        document.current_section_index += 1
    last_unfilled_field = next_unfilled_slot

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    print("output_context")
    print(output_context)
    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    global user

    last_unfilled_field = next_unfilled_slot
    last_intent = 'income_and_finances_fill'
    user.update_income_info(document)

    return jsonify(data)


def welcome(content):
    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": ["Hello!"]}}]
    return jsonify(data)


def exploit_deduction(content):
    parameters = content['queryResult']['parameters']
    current_intent = content['queryResult']['intent']['displayName']

    global responses
    global user
    global document
    global last_intent
    global last_unfilled_field
    global missed_deduction_values
    global previous_deduction_result

    error_field, error_message = error_checking(parameters, current_intent, last_unfilled_field)

    if error_field is not None or error_message is not None:
        deduction_result = copy.deepcopy(previous_deduction_result)
    else:
        deduction_result = None
        if len(missed_deduction_values) > 0:
            if document.deduction_user_info[last_unfilled_field] is None:
                if parameters['value'] != '':
                    document.deduction_user_info[last_unfilled_field] = parameters['value']
                elif parameters['dollar'] != '':
                    document.deduction_user_info[last_unfilled_field] = parameters['dollar']['amount']
            else:
                if parameters['value'] != '':
                    document.deduction_user_info[last_unfilled_field] += parameters['value']
                elif parameters['dollar'] != '':
                    document.deduction_user_info[last_unfilled_field] += parameters['dollar']['amount']

            missed_deduction_values.pop(0)
            deduction_result = copy.deepcopy(missed_deduction_values)

            if len(missed_deduction_values) == 0:
                deduction_result = 'deduction-success'
        elif current_intent == 'exploit_deduction.help' and document.deduction_stage != 'user_done':
            document.deduction_stage = 'user_done'

            for key, value in document.deduction_user_info.items():
                if value is None:
                    deduction_result = key
                    break

        elif document.deduction_stage == 'user_done':

            if document.deduction_user_info[last_unfilled_field] is None:
                if parameters['value'] != '':
                    document.deduction_user_info[last_unfilled_field] = parameters['value']
                elif parameters['dollar'] != '':
                    document.deduction_user_info[last_unfilled_field] = parameters['dollar']['amount']

            else:
                if parameters['value'] != '':
                    document.deduction_user_info[last_unfilled_field] += parameters['value']
                elif parameters['dollar'] != '':
                    document.deduction_user_info[last_unfilled_field] += parameters['dollar']['amount']
            for key, value in document.deduction_user_info.items():
                if value is None:
                    deduction_result = key
                    break

        else:
            deductions_and_values_found = parameters
            success = False

            possible_deduction_values = ['state-local-value', 'jury_duty_amount', 'account_401_value',
                                         'charitable-value', 'damage-cost', 'medical_value',
                                         'mortgage_value', 'roth-IRA-value', 'student_loans_value',
                                         'tuition_value']
            value_to_deduction_name = {'state-local-value': 'state-local-taxes', 'jury_duty_amount': 'jury-duty',
                                       'account_401_value': '401K', 'charitable-value': 'charitable-contribution',
                                       'medical_value': 'medical-dental-expenses', 'mortgage_value': 'mortgage',
                                       'roth-IRA-value': 'roth-IRA', 'damage-cost': 'damaged-property',
                                       'student_loans_value': 'student-loans', 'tuition_value': 'tuition'}

            missed_values = []
            #        deduction_result = document.update_slot(parameters, current_intent, last_unfilled_field)

            for possible_deduction_value in possible_deduction_values:
                if possible_deduction_value in deductions_and_values_found:
                    deduction_name = value_to_deduction_name[possible_deduction_value]
                    if len(deductions_and_values_found[possible_deduction_value]) == 0:
                        missed_values.append(possible_deduction_value)
                    else:
                        params = (deduction_name, deductions_and_values_found[possible_deduction_value])
                        print("params", params)
                        document.update_slot(params, current_intent, last_unfilled_field)
                        success = True

            if len(missed_values) > 0:
                deduction_result = missed_values
            elif success:
                deduction_result = 'deduction-success'
            else:
                deduction_result = 'deduction-failure'

    session = content['session']
    previous_deduction_result = copy.deepcopy(deduction_result)

    with open('response.json') as f:
        data = json.load(f)

    if deduction_result is None:
        document.current_section_index += 1
        if current_intent == 'exploit_deduction.help':
            response = "Well this is embarassing. I unfortunately can't find any more eligible deductions for you. But don't worry, we're almost done with your taxes!"
        else:
            type_chosen = document.compute_line_9()
            if type_chosen == 'standard deduction':
                response = "We're all done maximizing your deductions! Looks like you'll get more with standard deductions. Now we just have the easy parts left."
            else:
                response = "We're all done maximizing your deductions! Looks like you'll get more with itemized deductions. Now we just have the easy parts left."

        # Determine whether they need to do the refund or owe section
        if document.refund_user_info["overpaid"] <= 0:
            document.current_section_index += 1
            response += "You owe ${}. To pay, please visit https://www.irs.gov/payments. " \
                        "We're done with your refund/owe section. We're almost done! Please sign the form electronically".format(
                document.refund_user_info["amount-owed"])
        else:
            response += responses.get_next_response('amount-refunded', document)

    elif isinstance(deduction_result, list):
        missed_deduction_values = copy.deepcopy(deduction_result)
        followups = {'state-local-value': 'How much did you pay in those state and local taxes?',
                     'jury_duty_amount': 'What amount of money did you get from jury duty?',
                     'account_401_value': 'How much did you contribute to your 401K?',
                     'charitable-value': 'How much did you contribute to charity?',
                     'medical_value': 'How much did you spend on your healthcare?',
                     'mortgage_value': 'How much went towards your mortgage?',
                     'roth-IRA-value': 'How much did you contribute to your roth IRA?',
                     'student_loans_value': 'How much did you repay in student loans?',
                     'tuition_value': 'How much did tuition cost you?',
                     'damage-cost': 'How much were your losses valued at?'}
        response = followups[missed_deduction_values[0]]
    else:
        response = responses.get_next_response(deduction_result, document)
        print(response)

    if error_field is not None or error_message is not None:
        response = error_message + response
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    if isinstance(deduction_result, list):
        output_context = responses.generate_output_context('missed-deduction-value', 1, session, document)
    elif deduction_result is not None:
        output_context = responses.generate_output_context(deduction_result, 1, session, document)
    else:
        output_context = responses.generate_output_context('amount-refunded', 1, session, document)

    if isinstance(deduction_result, list):
        value_to_deduction_name = {'state-local-value': 'state-local-taxes', 'jury_duty_amount': 'jury-duty',
                                   'account_401_value': '401K', 'charitable-value': 'charitable-contribution',
                                   'medical_value': 'medical-dental-expenses', 'mortgage_value': 'mortgage',
                                   'roth-IRA-value': 'roth-IRA', 'damage-cost': 'damaged-property',
                                   'student_loans_value': 'student-loans', 'tuition_value': 'tuition'}
        last_unfilled_field = value_to_deduction_name[deduction_result[0]]
        print(last_unfilled_field)
    else:
        last_unfilled_field = deduction_result

    data['output_contexts'] = output_context

    global last_output_context
    last_output_context = output_context
    return jsonify(data)


def refund_and_owe(content):
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

    # Check for invalid input
    error_field, error_message = error_checking(parameters, current_intent, last_unfilled_field)

    if error_field is None and error_message is None:
        # first pass: update params on document object
        document.update_slot(parameters, current_intent, last_unfilled_field)

        # second pass: query next thing needed
        next_unfilled_slot = document.find_next_unfilled_slot()
    else:
        next_unfilled_slot = error_field
    last_unfilled_field = next_unfilled_slot

    # Set output contexts so that the next utterance can only match with the intents what we're asking about
    output_context = None
    if next_unfilled_slot in document.refund_user_info:
        response = responses.get_next_response(next_unfilled_slot, document)
        output_context = responses.generate_output_context(next_unfilled_slot, 1, session, document)
    else:
        response = "We're all done filling out your refund and amount to owe section. Let's move onto third party permissions! "
        response += responses.third_party['third-party']
        output_context = responses.generate_output_context('third-party', 1, session, document)
        document.current_section_index += 1
    if error_message:
        response = error_message

    last_unfilled_field = next_unfilled_slot

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    print("output_context:", output_context)
    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    global user

    last_intent = 'refund_and_owe'
    return jsonify(data)


def third_party(content):
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

    error_field, error_message = error_checking(parameters, current_intent, last_unfilled_field)

    if error_field is None and error_message is None:
        # first pass: update params on document object
        document.update_slot(parameters, current_intent, last_unfilled_field)

        # second pass: query next thing needed
        next_unfilled_slot = document.find_next_unfilled_slot()
    else:
        next_unfilled_slot = error_field
    last_unfilled_field = next_unfilled_slot

    # Set output contexts so that the next utterance can only match with the intents what we're asking about
    output_context = None
    if next_unfilled_slot in document.third_party_user_info:
        response = responses.get_next_response(next_unfilled_slot, document)
        output_context = responses.generate_output_context(next_unfilled_slot, 1, session, document)
    else:
        response = "We're all done filling out your third party section. All that's left is for you to sign, and we'll be done!"
        document.current_section_index += 1
    if error_message:
        response = error_message

    last_unfilled_field = next_unfilled_slot

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    print("output_context:", output_context)
    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    global user

    last_intent = 'third_party'
    return jsonify(data)


def autofill(content):
    """Automatically move to the income section."""
    global last_unfilled_field
    global responses
    global document

    document.update_dummy()

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']
    next_unfilled_slot = 'wages'
    last_unfilled_field = 'wages'
    response = responses.get_next_response(next_unfilled_slot, document)
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
    global last_output_context
    last_output_context = data['output_contexts']
    print(last_output_context)
    print(last_unfilled_field)

    return jsonify(data)


def autofill2(content):
    """Automatically move to the deductions section."""
    global last_unfilled_field
    global responses
    global document

    document.update_dummy()
    document.update_dummy2()

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']
    next_unfilled_slot = 'deduction-begin'
    last_unfilled_field = 'deduction-begin'
    response = responses.get_next_response(next_unfilled_slot, document)
    print("response:", response)
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
    global last_output_context
    last_output_context = data['output_contexts']
    print(last_output_context)
    print(last_unfilled_field)

    return jsonify(data)


def autofill3(content):
    """Automatically move to the refund/owe section."""
    global last_unfilled_field
    global responses
    global document

    print("autofill3")
    document.update_dummy()
    document.update_dummy2()
    document.update_dummy3()

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']
    next_unfilled_slot = 'amount-refunded'
    last_unfilled_field = 'amount-refunded'
    response = responses.get_next_response(next_unfilled_slot, document)
    print("response:", response)
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
    global last_output_context
    last_output_context = data['output_contexts']
    print(last_output_context)
    print(last_unfilled_field)

    return jsonify(data)


def fallback(content):
    global last_unfilled_field
    global responses
    global document
    global last_output_context
    global last_intent

    if last_unfilled_field == '':
        last_unfilled_field = document.demographics_slots_to_fill[0]

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']
    data['fulfillment_messages'] = [{"text": {"text": ["I didn't get that. Can you say it again?"]}}]
    if last_unfilled_field is not None:
        data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
        last_output_context = data['output_contexts']
        redo_response = responses.get_next_response(last_unfilled_field, document)
        if document.sections[document.current_section_index] == 'deductions':
            data['fulfillment_messages'] = [
                {"text": {"text": ["Sorry, we don't believe that qualifies you for a deduction. What other "
                                   "deductions you might want to claim? Otherwise, just let us know you need help!"]}}]
        else:
            data['fulfillment_messages'] = [
                {"text": {"text": ["Sorry, you may have entered an invalid value. " + redo_response]}}]

    else:
        print('something went wrong, last_unfilled_field is none')
    return jsonify(data)


def push_demographic_info_to_database(content):
    # change User object based on content

    # push to database
    users_ref = db.child('USERS')
    global user

    user_json = user.jsonify_user()
    users_ref.set(user_json)
    return


def misclassified_money_intent(content):
    global last_unfilled_field
    global responses
    global document
    global last_output_context
    print("misclassified money intent")

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
    redo_response = responses.get_next_response(last_unfilled_field, document)
    data['fulfillment_messages'] = [{"text": {"text": ["Sorry, this field only accepts nonnegative numerical values. "
                                                       "Please try again. " + redo_response]}}]

    return jsonify(data)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        content = request.json

        intent = content['queryResult']['intent']['displayName']
        print("intent:", intent)
        global last_unfilled_field
        global last_output_context
        global missed_deduction_values
        print("global last output context: " + str(last_output_context))

        if intent == 'goodbye' or 'goodbye' == content['queryResult']['queryText']:
            last_output_context = ""
            last_unfilled_field = ""
            print("global last output context: " + str(last_output_context))
            return clear()
        elif "monetary" in str(last_output_context) and "explain_term" not in intent:
            if intent != 'income_and_finances_fill.monetary_value' and intent != 'income_and_finances_fill.monetary_value_list':
                print(intent)
                return misclassified_money_intent(content)
            elif (
                    intent == 'income_and_finances_fill.monetary_value' or intent == 'income_and_finances_fill.monetary_value_list') \
                    and content['queryResult']['queryText'] == 'no':
                return misclassified_money_intent(content)
            elif (intent == 'income_and_finances_fill.monetary_value' or intent == 'income_and_finances_fill.monetary_value_list')  and (document.deduction_stage == 'user_done' or
                                                                          len(missed_deduction_values) > 0):
                return exploit_deduction(content)
            else:
                return income_finances_fill(content)
        elif intent == 'autofill':
            return autofill(content)
        elif intent == 'autofill2':
            return autofill2(content)
        elif intent == 'autofill3':
            return autofill3(content)
        elif intent == 'explain_term':
            return explain_term(content)
        elif intent.startswith('exploit_deduction'):
            return exploit_deduction(content)
        elif intent == 'explain_term - yes' or intent == 'explain_previous_term - yes':
            return explain_term_yes(content)
        elif intent == 'explain_term - repeat':
            return explain_term_repeat(content)
        elif intent == 'explain_previous_term':
            return explain_term(content, unstandardize_token(last_unfilled_field))
        elif intent == 'income_and_finances':
            return income_finances_fill(content)
        elif intent == 'refund_and_owe':
            return refund_and_owe(content)
        elif intent.startswith('third_party'):
            return third_party(content)
        elif intent.startswith('demographics_fill'):
            return demographics_fill(content)
        elif intent.startswith('income_and_finances_fill'):
            return income_finances_fill(content)
        elif intent.startswith('refund_and_owe'):
            return refund_and_owe(content)
        elif intent == 'Default Welcome Intent':
            return welcome(content)
        else:
            return fallback(content)

    else:
        return "Welcome to CPai!"


@app.route('/document', methods=['GET'])
def getDocument():
    global document

    payload = dict()

    payload['demographics'] = {
        'user': document.demographic_user_info,
        'spouse': document.demographic_spouse_info,
        'dependents': [dep.slots for dep in document.dependents]
    }

    payload['income'] = {
        'user': document.income_user_info
    }

    response = make_response(payload)
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/jpg', methods=['GET'])
def getJpg():
    global document
    fields = pdf.fillInFields(document)
    pdf.generatePdf(fields)
    pdf.generateImage()
    return send_file('./page.jpg')


@app.route('/pdf', methods=['GET'])
def getPdf():
    global document
    fields = pdf.fillInFields(document)
    pdf.generatePdf(fields)
    return send_file('./f1040.pdf')


if __name__ == "__main__":
    app.run(port=5000, debug=True)