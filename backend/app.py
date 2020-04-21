"""
App.py
Contains the Flask web application that runs our business logic
DialogFlow fulfilment webhook routes through home(), which uses the extracted intent to direct to the appropriate
    subfunction that performs slot extraction, updates the user info, and redirects the conversational flow
Also allows for communication with the Firebase database to extract terminology definitions
"""


from flask import Flask, render_template, redirect, url_for, request, jsonify, make_response, send_file
from document import Document
from user import User
from response import Response
import pyrebase
import pprint
import json
import copy
import pdf
import numpy as np

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
    """Replace any underscores with spaces."""
    return token.replace("_", " ")


def standardize_token(token):
    """Replace any dashes and spaces with underscores."""
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

    # Open the template response form
    with open('response.json') as f:
        data = json.load(f)

    next_unfilled_slot = document.find_next_unfilled_slot()

    # Get the response for the question inquiring about the next field
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

    # Open the template response form
    with open('response.json') as f:
        data = json.load(f)

    # Load the dictionary with all of our terms 
    firebase_data = db.child("TERMINOLOGY").get().val()

    # In case the user did not specify a term, use the last unfilled slot
    next_unfilled_slot = document.find_next_unfilled_slot()

    # Get the response for the question inquiring about the next field
    if last_unfilled_field == "":
        response = "First we need to gather some basic demographic information. Tell me your name, age, and occupation."
        output_context = responses.generate_output_context("given-name", 1, session, document)
    else:
        response = responses.get_next_response(next_unfilled_slot, document)
        output_context = responses.generate_output_context(last_unfilled_field, 1, session, document)

    # data['fulfillment_messages'] = [
    #     {
    #         "text": {
    #             "text": [
    #                 "I am sorry to hear that. Here is a link that should provide you with some more details: \n" + firebase_data[last_term_explained]["link"] + "\n"
    #             ]
    #         }
    #     },
    #     # {
    #     #     "card": {
    #     #         "buttons": [
    #     #             {
    #     #                 "text": firebase_data[last_term_explained]["link"],
    #     #                 "postback": firebase_data[last_term_explained]["link"]
    #     #             }
    #     #         ]
    #     #     }
    #     # },
    #     {
    #         "text": {
    #             "text": [
    #                 "Whenever you are ready, let's continue. " + response
    #             ]
    #         }
    #     }, ]

    data['fulfillment_messages'] = [{"text": {"text": ["I am sorry to hear that. Here is a link that should provide you with some more details: \n" + firebase_data[last_term_explained]["link"] + "\n" + "Whenever you are ready, let's continue. " + response]}}]

    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    return jsonify(data)


def explain_term(content, extract=None):
    """
    Explain a term that the user is asking about. 
    The extract parameter is for when explain_term needs to be called
    from the server-end instead of being called from DialogFlow.
    """
    global last_term_explained

    # print(content, extract)
    # Grab the term that the user is confused about
    if extract is None:
        extract = content['queryResult']['parameters']['terminology']

    # Set last_term_explained global so it can be used in other functions
    tokenized_extract = standardize_token(extract)
    last_term_explained = tokenized_extract

    print(tokenized_extract)
    print(last_term_explained)

    # Load firebase dictionary with all of the terms
    firebase_data = db.child("TERMINOLOGY").get().val()

    # Open the template response form
    with open('response.json') as f:
        data = json.load(f)

    # No definition exists
    if tokenized_extract not in firebase_data:
        data['fulfillment_messages'] = \
            [{"text": {"text": [
                "Sorry, I don't have a working definition for " + extract +
                ". Do you want to go back to filling out the form?"]}}]
    # Definition exists
    else:
        response = "Great question, " + extract + " is " + firebase_data[tokenized_extract][
            "definition"] + ". Does that make sense?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    # Special case for filing-status because it's a long description that doesn't fit the format of "X means Y".
    if extract == "filing status":
        global document
        if document.demographic_user_info['is-married']:
            response = "If you file jointly, you and your spouse will fill out one tax form together. If you file " \
                       "separately, each of you will fill out your own tax form. Most of the time, we'll encourage " \
                       "you to file together, but if one of you has significant itemized deductions, it may be better" \
                       " to file together. Later on, we'll let you know if it's better to file separetely. Does that " \
                       "make sense?"
            data['fulfillment_messages'] = [{"text": {"text": [response]}}]
        else:
            response = "If you file had a spouse die within the past two years, you can file as a qualifying widower," \
                       "which brings certain tax deductions.  Does that make sense?"
            data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    # Special case for deduction because it's not a precise definition
    elif 'deduction' in extract:
        response = "A deduction is essentially a discount on your taxes that you get by performing actions that " \
                   "the government sees as bettering society overall. Does that make sense?"
        data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    global last_intent
    last_intent = 'explain_term'
    return jsonify(data)


def clear():
    """Clear all data so that we can start a fresh profile whenever we need"""
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
    return jsonify(data)


def error_checking(parameters, intent, last_unfilled, queryText=None):
    """
    Checks for invalid parameters given the intent that we are inquiring about.
    If there is an error, return (field-name, error-message).
    Otherwise, return (None, None)
    """
    global document

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

    # Address: zip code should be 5 numbers
    if 'address' in intent:
        value = str(parameters['zip-code'])
        if len(value) != 5:
            return 'street_address', 'You entered an invalid ZIP code. A valid ZIP code consists of five numbers. '
        for digit in value:
            if digit not in digits:
                return 'street_address', 'You entered an invalid ZIP code. A valid ZIP code consists of five numbers. '

    # SSN should be 9 digits
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
                    return 'social_security', 'You entered an invalid SSN. Valid SSNs are exactly ' \
                                              'nine numbers in length. '

            elif digit == '-':
                num_hyphens += 1
            else:
                return 'social_security', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

        if num_digits != 9:
            return 'social_security', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length. '

    # Spouse-SSN should be 9 digits
    elif 'spouse_SSN' in intent:
        if len(str(parameters['spouse-ssn'])) != 11:  # accounts for the trailing '.0'
            return 'spouse-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length.'
    
    # Dependent-SSN should be 9 digits
    elif 'dependent_ssn' in intent:
        if len(str(parameters['dependent-ssn'])) != 11:
            return 'dependent-ssn', 'You entered an invalid SSN. Valid SSNs are exactly nine numbers in length.'

    # Monetary-value intent should have non-negative numbers
    elif intent == 'income_and_finances_fill.monetary_value':
        dollar_value = str(parameters['value'])
        dollar_value_2 = ''
        if parameters['dollar'] != '':
            dollar_value_2 = str(parameters['dollar']["amount"])
        if '-' in dollar_value or '-' in dollar_value_2:
            return last_unfilled, 'You entered a negative dollar amount. Only non-negative values are allowed. '

        try:
            float(dollar_value)
        except ValueError:
            try:
                float(dollar_value_2)
            except ValueError:
                return last_unfilled, 'You entered an invalid dollar amount. Non-numeric characters are not allowed. '

    # Monetary-value-list should have non-negative numbers
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
            if '-' in dollar_value:
                return last_unfilled, 'You entered a negative dollar amount. Only non-negative values are allowed. '

            try:
                float(dollar_value)
            except ValueError:
                return last_unfilled, 'You entered an invalid dollar amount. Non-numeric characters are not allowed. '

    # Routing number should be 9 digits
    if intent == 'refund_and_owe.number_value' and last_unfilled == 'routing-number':
        if len(str(parameters['number'])) != 11: # accounts for the trailing '.0'
            return last_unfilled, 'You entered an invalid routing number. Please type in exactly 9 digits for ' \
                                  'your routing number.'
    # Account number should be 17 digits
    elif intent == 'refund_and_owe.number_value' and last_unfilled == 'account-number':
        num = str(parameters['number'])
        if not num.endswith('e+16'):
            return last_unfilled, 'You entered an invalid account number. Please type in exactly 17 digits ' \
                                  'for your routing number.'
    # User tries to get more money refunded than they're allowed
    elif intent == 'refund_and_owe.number_value' and (
            last_unfilled == 'overpaid-applied-tax' or last_unfilled == 'amount-refunded'):
        if type(parameters['number']) != str and (parameters['number'] > document.refund_user_info["overpaid"]):
            return last_unfilled, 'You cannot use an amount greater than the amount you overpaid. Please give a\
                 number equal to or less than ${}.'.format(document.refund_user_info["overpaid"])

    # Phone number should be 10 digits
    if intent == 'third_party.phone_number':
        if len(str(parameters['phone-number'])) != 10:
            return last_unfilled, 'You entered an invalid phone number. Please type in exactly 10 digits.'
    # PIN should be 5 digits
    elif intent == 'third_party.pin':
        if len(str(parameters['PIN'])) != 7:
            return last_unfilled, 'You entered an invalid PIN. Please type in exactly 5 digits.'

    # Email should be formatted with @
    # Phone number should be 10 digits
    if intent == 'demographics_fill.email_phone_number':
        email = str(parameters['email'])
        phone_number = str(parameters["user-phone-number"])

        if email != '' and '@' not in email:
            return 'email', 'You entered an invalid email.'
        
        if phone_number != '' and len(phone_number) != 10:
            return 'user-phone-number', 'You entered an invalid phone number. Please type in exactly 10 digits.'

    # No errors
    return None, None


def demographics_fill(content):
    """Handle any DialogFlow intents that deal with the demographics section."""
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
        # Update params on document object
        document.update_slot(parameters, current_intent, last_unfilled_field)

        # Query next thing needed
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
            name = document.dependents[-1].slots['dependent-given-name'][0]
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

    print(document.dependents)
    # Open the template response form
    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    global user

    last_intent = 'demographics_fill'
    user.update_demographic_info(document)
    return jsonify(data)


def income_finances_fill(content):
    """Handle any DialogFlow intents that deal with the income section."""
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

    # Check for errors in the values returned from DF
    error_field, error_message = error_checking(parameters, current_intent, last_unfilled_field)

    if error_field is None and error_message is None:
        # Update params on document object
        document.update_slot(parameters, current_intent, last_unfilled_field)

        # Query next thing needed
        next_unfilled_slot = document.find_next_unfilled_slot()
    else:
        next_unfilled_slot = error_field

    # No more slots left to ask about income, move to next section
    if next_unfilled_slot is None:
        response = "We're all done filling out your income and finances. Let's move onto calculating your deductions! "
        last_intent = 'income_and_finances_fill.social_security_benefits'
    # Still slots remaining for income, ask about income again
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

    # Open the template response form
    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
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
    """Handle all DialogFlow intents that deal with deductions."""
    parameters = content['queryResult']['parameters']
    current_intent = content['queryResult']['intent']['displayName']

    global responses
    global user
    global document
    global last_intent
    global last_unfilled_field
    global missed_deduction_values
    global previous_deduction_result

    value = 0

    # Check for invalid parameter values, such as a negative dollar amount
    error_field, error_message = error_checking(parameters, current_intent, last_unfilled_field)

    # If error is found, ignore current result and retain old deduction information to prompt user again
    if error_field is not None or error_message is not None:
        deduction_result = copy.deepcopy(previous_deduction_result)

    # No errors, proceed with deduction handling
    else:
        deduction_result = None
        # List that contains the deductions that the user claimed on their own, but for which they did not provide
        # a dollar value (i.e., I paid state and local taxes OR I had healthcare expenses)
        if len(missed_deduction_values) > 0:
            # Fill document with the value extracted from DF
            # If the value is None, we have yet to determine whether the user qualifies for that deduction
            if document.deduction_user_info[last_unfilled_field] is None:
                if len(parameters['value']) != 0:
                    document.deduction_user_info[last_unfilled_field] = np.sum(parameters['value'])
                elif len(parameters['dollar']) != 0:
                    val = 0
                    for item in parameters['dollar']:
                        val += item['amount']
                    document.deduction_user_info[last_unfilled_field] = val
                    value = copy.deepcopy(val)
            # Field is not empty, add to existing value
            else:
                if len(parameters['value']) != 0:
                    document.deduction_user_info[last_unfilled_field] += np.sum(parameters['value'])
                elif len(parameters['dollar']) != 0:
                    val = 0
                    for item in parameters['dollar']:
                        val += item['amount']
                    document.deduction_user_info[last_unfilled_field] += val
                    value = copy.deepcopy(val)
            # Took care of the missed dollar value for the deduction, so no need to worry about it anymore
            missed_deduction_values.pop(0)

            # Store the array of pending missed deduction values
            deduction_result = copy.deepcopy(missed_deduction_values)

            # All user-claimed deductions have currently been assigned a dollar value, so go back to normal flow
            if len(missed_deduction_values) == 0:
                deduction_result = 'deduction-success'

        # User is asking for help with deductions right off the bat, without trying to claim deductions on their own
        elif current_intent == 'exploit_deduction.help' and document.deduction_stage != 'user_done':
            document.deduction_stage = 'user_done'

            # Get the next deduction item that we should ask them about
            for key, value in document.deduction_user_info.items():
                if value is None:
                    deduction_result = key
                    break

        # AFTER user has asked for help: prompt for deduction information sequentially
        elif document.deduction_stage == 'user_done':
            # Set the values extracted from DF response
            # Field is empty
            if document.deduction_user_info[last_unfilled_field] is None:
                if len(parameters['value']) != 0:
                    document.deduction_user_info[last_unfilled_field] = np.sum(parameters['value'])
                    value = np.sum(parameters['value'])
                elif len(parameters['dollar']) != 0:
                    val = 0
                    for item in parameters['dollar']:
                        val += item['amount']
                    document.deduction_user_info[last_unfilled_field] = val
                    value = copy.deepcopy(val)
            # Field is not empty, add to existing value
            else:
                if len(parameters['value']) != 0:
                    document.deduction_user_info[last_unfilled_field] += np.sum(parameters['value'])
                    value = np.sum(parameters['value'])
                elif len(parameters['dollar']) != 0:
                    val = 0
                    for item in parameters['dollar']:
                        val += item['amount']
                    document.deduction_user_info[last_unfilled_field] += val
                    value = copy.deepcopy(val)
            
            # Find next deduction item to inquire about
            for key, value in document.deduction_user_info.items():
                if value is None:
                    deduction_result = key
                    break

        # User claims deductions on their own without our help; we make sure it qualifies and we handle that deduction
        else:
            # Parameters given by DialogFlow should hold relevant deductions and corresponding dollar values
            deductions_and_values_found = parameters

            success = False

            # Deductions that we handle and they can qualify for
            possible_deduction_values = ['state-local-value', 'jury_duty_amount', 'account_401_value',
                                         'charitable-value', 'damage-cost', 'medical_value',
                                         'mortgage_value', 'roth-IRA-value', 'student_loans_value',
                                         ]

            # Maps the DialogFlow parameter given to us by the JSON object to its name in the Document class
            value_to_deduction_name = {'state-local-value': 'state-local-taxes', 'jury_duty_amount': 'jury-duty',
                                       'account_401_value': '401K', 'charitable-value': 'charitable-contribution',
                                       'medical_value': 'medical-dental-expenses', 'mortgage_value': 'mortgage',
                                       'roth-IRA-value': 'roth-IRA', 'damage-cost': 'damaged-property',
                                       'student_loans_value': 'student-loans'}

            # List will hold any deductions claimed by the user for which they didn't provide dollar value
            missed_values = []

            # Loop through and check if any reported deductions are valid
            for possible_deduction_value in possible_deduction_values:
                if possible_deduction_value in deductions_and_values_found:
                    deduction_name = value_to_deduction_name[possible_deduction_value]
                    print(deduction_name)

                    # If user claimed a deduction on their own but forgot to include dollar value, add to the
                    # missed_values vector and handle it next time
                    if len(deductions_and_values_found[possible_deduction_value]) == 0:
                        missed_values.append(possible_deduction_value)

                    elif (parameters[deduction_name] is None) or (parameters[deduction_name] == '') or (len(parameters[deduction_name]) == 0):
                        success = False

                    # Otherwise, if they qualify for deduction and have a valid dollar value, update informatoin
                    else:
                        params = (deduction_name, deductions_and_values_found[possible_deduction_value])
                        test = document.update_slot(params, current_intent, last_unfilled_field)
                        value = copy.deepcopy(test)
                        success = True

            # User claimed deductions without designating dollar value, will handle in next question
            if len(missed_values) > 0:
                deduction_result = missed_values

            # User claimed valid deductions and had corresponding dollar value for each
            elif success:
                deduction_result = 'deduction-success'

            # User claimed an invalid deduction (i.e., "I walked my neighbor's dog")
            else:
                deduction_result = 'deduction-failure'

    session = content['session']
    previous_deduction_result = copy.deepcopy(deduction_result)

    # Load the JSON object template that will be sent back to DialogFlow
    with open('response.json') as f:
        data = json.load(f)

    # There are no deductions left that the user could possibly qualify for. Move onto the next section.
    if deduction_result is None:
        # Increment section index to the refund and owe section
        document.current_section_index += 1

        # Calculate best option (standard or itemized)
        type_chosen = document.compute_line_9()
        document.truncate_decimals()

        # Inform user about whether the standard or itemized deduction will save them more money:
        if type_chosen == 'standard deduction':
            response = "Looks like you'll get more with standard deductions. Now we just have the easy parts left."
        else:
            response = "Looks like you'll get more with itemized deductions. Now we just have the easy parts left."

        # User asked for help but they already claimed all possible deductions so agent can't help them at this point
        if current_intent == 'exploit_deduction.help':
            addition = "Well this is embarassing. I unfortunately can't find any more eligible deductions for you. " \
                       "Don't worry though! "

        else:
            addition = "We're all done maximizing your deductions! "

        response = addition + response

        document.compute_overpaid_amount()
        # Determine whether they need to do the refund or owe section
        if document.refund_user_info["overpaid"] <= 0:
            response += "You owe ${}. To pay, please visit https://www.irs.gov/payments. " \
                        "We're done with your refund/owe section! ".format(document.refund_user_info["amount-owed"])
            response += responses.third_party['third-party']
            document.current_section_index += 1
            output_context = responses.generate_output_context(
                'third-party', 1, session, document)
        else:
            response += responses.get_next_response('amount-refunded', document)

    
    # User claimed valid deduction without specifying dollar value. Find the appropriate follow-up question by
    # remembering original context
    elif isinstance(deduction_result, list):
        missed_deduction_values = copy.deepcopy(deduction_result)

        # Maps the pertinent deduction to its followup
        followups = {'state-local-value': 'How much did you pay in those state and local taxes?',
                     'jury_duty_amount': 'What amount of money did you get from jury duty?',
                     'account_401_value': 'How much did you contribute to your 401K?',
                     'charitable-value': 'How much did you contribute to charity?',
                     'medical_value': 'How much did you spend on your healthcare?',
                     'mortgage_value': 'How much went towards your mortgage?',
                     'roth-IRA-value': 'How much did you contribute to your roth IRA?',
                     'student_loans_value': 'How much did you repay in student loans?',
                     'damage-cost': 'How much were your losses valued at?'}
        response = followups[missed_deduction_values[0]]

    # Proceed as normal through the deductions flow
    else:
        if deduction_result == "deduction-success":
            response = 'Congrats, you potentially saved yourself $' + str('%.2f' % value) + '! What other deductions do you want to claim? If you want help from us, just say so!'
        else:
            response = responses.get_next_response(deduction_result, document)

    # Check for errors that might happen with the values that DF returned
    if error_field is not None or error_message is not None:
        response = error_message + response
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]

    # Set appropriate output contexts
    # If the deduction we're going to inquire about next is a list, that means that the user forgot to specify dollar
    # value, so we set the output context appropriately for the followup
    if isinstance(deduction_result, list):
        output_context = responses.generate_output_context('missed-deduction-value', 1, session, document)

    # Either user claimed valid deduction with dollar value OR wanted help OR claimed invalid deduction
    elif deduction_result is not None:
        output_context = responses.generate_output_context(deduction_result, 1, session, document)

    # User finished deductions section and needs to move on to refund-and-owe
    else:
        output_context = responses.generate_output_context('amount-refunded', 1, session, document)

    # If deduction claimed didn't have corresponding dollar value, remember it for the future because the followup
    # will provide information about it
    if deduction_result is None:
        if document.refund_user_info["overpaid"] <= 0:
            last_unfilled_field = 'third-party'
            output_context = responses.generate_output_context(
                'third-party', 1, session, document)
        else:
            last_unfilled_field = 'amount-refunded'
    elif isinstance(deduction_result, list):
        value_to_deduction_name = {'state-local-value': 'state-local-taxes', 'jury_duty_amount': 'jury-duty',
                                   'account_401_value': '401K', 'charitable-value': 'charitable-contribution',
                                   'medical_value': 'medical-dental-expenses', 'mortgage_value': 'mortgage',
                                   'roth-IRA-value': 'roth-IRA', 'damage-cost': 'damaged-property',
                                   'student_loans_value': 'student-loans'}
        last_unfilled_field = value_to_deduction_name[deduction_result[0]]
    else:
        last_unfilled_field = deduction_result

    data['output_contexts'] = output_context

    global last_output_context
    last_output_context = output_context
    return jsonify(data)


def refund_and_owe(content):
    """Handle any DialogFlow intents that deal with the refund and owe section."""

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
        # Update params on document object

        document.update_slot(parameters, current_intent, last_unfilled_field)

        # Query next thing needed
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
        response = "We're all done filling out your refund and amount to owe section. " \
                   "Let's move onto third party permissions! "
        response += responses.third_party['third-party']
        output_context = responses.generate_output_context('third-party', 1, session, document)
        next_unfilled_slot = 'third-party'
        document.current_section_index += 1
    if error_message:
        response = error_message

    last_unfilled_field = next_unfilled_slot

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = output_context
    global last_output_context
    last_output_context = output_context
    global user

    last_intent = 'refund_and_owe'
    return jsonify(data)


def third_party(content):
    """Handle any DialogFlow intents that deal with the third party permission section."""
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
        # Update params on document object
        document.update_slot(parameters, current_intent, last_unfilled_field)

        # Query next thing needed
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
        response = "We're all done filling out your third party section. You're now finished with your entire 1040! All that's left is for you to export as a pdf."
        document.current_section_index += 1
    if error_message:
        response = error_message

    last_unfilled_field = next_unfilled_slot

    with open('response.json') as f:
        data = json.load(f)

    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
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

    # Fill out the document object
    document.update_dummy()

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']

    # Set the next questions to be about wages (the first item in the income section)
    next_unfilled_slot = 'wages'
    last_unfilled_field = 'wages'
    response = responses.get_next_response(next_unfilled_slot, document)

    # Set the output json 
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
    global last_output_context
    last_output_context = data['output_contexts']
    return jsonify(data)


def autofill2(content):
    """Automatically move to the deductions section."""
    global last_unfilled_field
    global responses
    global document

    # Fill out the document object
    document.update_dummy()
    document.update_dummy2()

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']

    # Set the next questions to be about deductions
    next_unfilled_slot = 'deduction-begin'
    last_unfilled_field = 'deduction-begin'
    response = responses.get_next_response(next_unfilled_slot, document)

    # Set the output json
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
    global last_output_context
    last_output_context = data['output_contexts']
    return jsonify(data)


def autofill3(content):
    """Automatically move to the refund/owe section."""
    global last_unfilled_field
    global responses
    global document

    # Fill out the document object
    document.update_dummy()
    document.update_dummy2()
    document.update_dummy3()

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']

     # Set the next questions to be about the refund section
    next_unfilled_slot = 'amount-refunded'
    last_unfilled_field = 'amount-refunded'
    response = responses.get_next_response(next_unfilled_slot, document)

    # Set the output json
    data['fulfillment_messages'] = [{"text": {"text": [response]}}]
    data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
    global last_output_context
    last_output_context = data['output_contexts']
    return jsonify(data)


def fallback(content):
    """Error handling for when Dialogflow could not categorize the utterance
    into any intent (while factoring in output contexts)."""
    global last_unfilled_field
    global responses
    global document
    global last_output_context
    global last_intent

    # If last_unfilled_field has not been set yet, set it to the first slot we
    # ever inquire about (the first slot of demographics)
    if last_unfilled_field == '':
        last_unfilled_field = document.demographics_slots_to_fill[0]

    with open('response.json') as f:
        data = json.load(f)

    session = content['session']
    data['fulfillment_messages'] = [{"text": {"text": ["I didn't get that. Can you say it again?"]}}]

    # Reset the output context (since it only lasts one round of utterances) so the user can match to the proper intent 
    # Grab the appropriate question tfor the slot we are inquiring about
    if last_unfilled_field is not None:
        data['output_contexts'] = responses.generate_output_context(last_unfilled_field, 1, session, document)
        last_output_context = data['output_contexts']
        redo_response = responses.get_next_response(last_unfilled_field, document)

        # If we get to fallback in the deductions section, assume that they inquired about an invalid deduction
        if document.sections[document.current_section_index] == 'deductions':
            data['fulfillment_messages'] = [
                {"text": {"text": ["Sorry, we don't believe that qualifies you for a deduction. What other "
                                   "deductions you might want to claim? Otherwise, just let us know you need help!"]}}]
        else:
            data['fulfillment_messages'] = [
                {"text": {"text": ["Sorry, you may have entered an invalid value. " + redo_response]}}]

    return jsonify(data)

def misclassified_money_intent(content):
    """
    Handle situations in income where Dialogflow incorrectly classifies as a money intention because the user put in a
    weird value. Must be handled differently than error checking because the intent itself is wrong, not just the value.
    """
    global last_unfilled_field
    global responses
    global document
    global last_output_context

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
    """Primary link that DialogFlow fulfillment is connected to and will make a call
    to every time an intent is matched with webhook fulfillment turned on."""
    if request.method == 'POST':
        content = request.json

        intent = content['queryResult']['intent']['displayName']
        global last_unfilled_field
        global last_output_context
        global missed_deduction_values

        print("INTENT", intent)

        # If user says goodbye, clear all information to start fresh
        if intent == 'goodbye' or 'goodbye' == content['queryResult']['queryText']:
            last_output_context = ""
            last_unfilled_field = ""
            return clear()
        # Handle bug where DF misclassifies an intent as a money intent
        elif "monetary" in str(last_output_context) and "explain_term" not in intent and "explain_previous_term" not in intent:
            if intent != 'income_and_finances_fill.monetary_value' and \
                    intent != 'income_and_finances_fill.monetary_value_list':
                return misclassified_money_intent(content)
            elif (intent == 'income_and_finances_fill.monetary_value' or
                  intent == 'income_and_finances_fill.monetary_value_list') \
                    and content['queryResult']['queryText'] == 'no':
                return misclassified_money_intent(content)
            elif (intent == 'income_and_finances_fill.monetary_value' or
                  intent == 'income_and_finances_fill.monetary_value_list')  \
                    and (document.deduction_stage == 'user_done' or len(missed_deduction_values) > 0):
                return exploit_deduction(content)
            else:
                return income_finances_fill(content)
        
        # Return functions that correspond to each dialogflow intent (or category of dialogflow intents)
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
    """Used by the frontend to grab the relevant document information to display on the tax form."""
    global document
    # document.truncate_decimals()
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
    """Used by the frontend to generate a jpg for the user."""
    global document
    fields = pdf.fillInFields(document)
    pdf.generatePdf(fields, document)
    pdf.generateImage()
    return send_file('./page.jpg')


@app.route('/pdf', methods=['GET'])
def getPdf():
    """Used by the frontend to generate a pdf for the user."""
    global document
    fields = pdf.fillInFields(document)
    pdf.generatePdf(fields, document)
    return send_file('./f1040_signed.pdf')


if __name__ == "__main__":
    app.run(port=5000, debug=True)
