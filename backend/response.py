"""
Response.py
Class that houses the different responses that control the DialogFlow conversation
Composed of different dictionaries corresponding to the different sections of
    the 1040 document (demographics, income, deductions, spouse info, dependent info, etc.)
In each dictinoary, there is a mapping of term/field in the Document class to the question that will fulfill the info
In addition, there is a mapping of terms to output contexts, which will help set the next DialogFlow context
"""

class Response:
    def __init__(self):
        # Demographics questions for user only
        self.demographics = {
            'given-name': 'What is your first name?',
            'last-name': 'What is your last name?',
            'age': 'How old are you?',
            'occupation': 'What is your occupation? If you are retired, please say so.',
            'street_address': 'What is your full home address and ZIP code?',
            'city': 'What city do you live in?',
            'geo-country': 'What country do you live in?',
            'geo-state': 'What state do you live in?',
            'zip-code': "What's your ZIP code?",
            'social_security': 'Please type in your social security number (SSN).',
            'email': 'What is your email?',
            'user-phone-number': 'What is your phone number?',
            'is-married': 'Are you currently married?',
            'num_dependents': "How many dependents are you claiming?",
            'filing_status_married': 'Are you filing jointly with your spouse or filing separately?',
            'filing_status_HOH_widower': "Have you had a spouse die within the last two tax years?",
            'dual_status_alien': "Are you a dual-status alien?",
            'blind': "Are you blind?",
            'lived-apart': "Have you lived apart from your spouse for all of this year?",
            'claim-you-dependent': 'Can someone claim you as a dependent?',
            'claim-spouse-dependent': 'Can someone claim your spouse as a dependent?',
            'spouse-itemize-separate': 'Is your spouse itemizing on a separate return?',
        }

        # Demographics questions for user's spouse, if applicable
        self.demographics_spouse = {
            'spouse-given-name': "Since you're married, I will need some of your spouse's information. "
                                 "What is your spouse's name, age, and occupation?",
            'spouse-last-name': "What is your spouse's last name?",
            'spouse-age': "What is your spouse's age?",
            'spouse-occupation': "What is your spouse's occupation?",
            'spouse-ssn': "Please type in your spouse's SSN.",
            'spouse-blind': 'Is your spouse blind?',
            'claim-spouse-dependent': 'Can someone claim your spouse as a dependent?',
            'spouse-itemize-separate': 'Is your spouse itemizing on a separate return?'
        }

        # Mapping of the next field that needs to be filled to the proper output context for DialogFlow
        self.slot_to_output_contexts = { 
            'given-name': 'prompt_name',
            'last-name': 'prompt_name',
            'age': 'prompt_name',
            'occupation': 'prompt_name',
            'street_address': 'prompt_address',
            'geo-state': 'prompt_address',
            'city': 'prompt_address',
            'zip-code': 'prompt_address',
            'social_security': 'prompt_social_security',
            'email': 'prompt_email_phone_number',
            'user-phone-number': 'prompt_email_phone_number', 
            'is-married': 'prompt_is_married',
            'dual_status_alien': "prompt_dual_status_alien",
            'blind': 'prompt_blind',
            'lived-apart': 'prompt_lived_apart',
            'num_dependents': 'prompt_num_dependents',
            'dependent-citizenship': 'prompt_dependent_citizenship',
            'filing_status_married': 'prompt_filing_status_married',
            'filing_status_HOH_widower': 'prompt_filing_status_widower',
            'spouse-given-name': "prompt_spouse_name_age",
            'spouse-last-name': "prompt_spouse_name_age",
            'spouse-age': "prompt_spouse_name_age",
            'spouse-occupation':'prompt_spouse_name_age',
            'spouse-ssn': "prompt_spouse_SSN",
            'spouse-blind': "prompt_spouse_blind",
            'dependent-given-name': "prompt_dependent_info",
            'dependent-last-name': "prompt_dependent_info",
            'dependent-age': "prompt_dependent_info",
            'dependent-relation': "prompt_dependent_info",
            'dependent-ssn': "prompt_dependent_ssn",
            'claim-you-dependent': 'prompt-claim-you-dependent',
            'claim-spouse-dependent': 'prompt-claim-spouse-dependent',
            'spouse-itemize-separate': 'prompt-spouse-itemize-separate',
            'change_field_value': "prompt_change_field_value",
            'change_field_confirm': "prompt_change_field_confirm",
            'confirm_section': "prompt_confirm",
            'wages': "prompt_monetary_value_list",
            'tax-exempt-interest': 'prompt_monetary_value_list',
            'taxable-interest': 'prompt_monetary_value_list',
            'has-1099-R': 'prompt_has_1099_R',
            'pensions-and-annuities': 'prompt_monetary_value_list',
            'pensions-and-annuities-taxable': 'prompt_monetary_value_list',
            'capital-gains': "prompt_gains_losses",
            'taxable-refunds': "prompt_monetary_value",
            'total-qualified-business-income': "prompt_monetary_value",
            'business-income': "prompt_gains_losses",
            'unemployment-compensation':  'prompt_monetary_value',
            'other-income': 'prompt_monetary_value',
            'owns-business': 'prompt_owns_business',
            'owns-stocks-bonds': "prompt_stocks_bonds",
            'pass-through-business': 'prompt_pass_through_business',
            'has-1099-DIV': 'prompt_has_1099_DIV',
            'qualified-dividends': 'prompt_monetary_value',
            'ordinary-dividends': 'prompt_monetary_value',
            'IRA-distributions': 'prompt_monetary_value',
            'IRA-distributions-taxable': 'prompt_monetary_value',
            'educator-expenses': 'prompt_monetary_value',
            'business-expenses': 'prompt_monetary_value',
            'health-savings-deductions': 'prompt_monetary_value',
            'moving-expenses-armed-forces': 'prompt_monetary_value',
            'self-employed-health-insurance': 'prompt_monetary_value',
            'IRA-deductions': 'prompt_monetary_value',
            'student-loan-interest-deduction': 'prompt_monetary_value',
            'tuition-fees': 'prompt_monetary_value',
            'federal-income-tax-withheld': 'prompt_monetary_value',
            'ss-benefits': 'prompt_monetary_value_list',
            'schedule-2-line-3': 'prompt_monetary_value',
            'schedule-3-line-7': 'prompt_monetary_value',
            'schedule-2-line-10': 'prompt_monetary_value',
            'schedule-3-line-14': 'prompt_monetary_value',
            'deduction-begin': 'prompt_deduction_begin',
            'account_401': 'prompt_monetary_value_list',
            'deduction-success': 'prompt_deduction_begin',
            'deduction-failure': 'prompt_deduction_begin',
            'charitable-contribution': 'prompt_monetary_value_list',
            'state-local-taxes': 'prompt_monetary_value_list',
            'mortgage': 'prompt_monetary_value_list',
            'roth-IRA': 'prompt_monetary_value_list',
            'damaged-property': 'prompt_monetary_value_list',
            'medical-dental-expenses': 'prompt_monetary_value_list',
            'jury-duty': 'prompt_monetary_value_list',
            'student-loans': 'prompt_monetary_value_list',
            'amount-refunded': 'prompt_refund_number_value',
            'overpaid-applied-tax': 'prompt_refund_number_value',
            'direct-deposit': 'prompt_refund_bool',
            'account-type': 'prompt_type_of_account',
            'routing-number': 'prompt_refund_number_value',
            'account-number': 'prompt_refund_number_value',
            'estimated-tax-penalty': 'prompt_refund_number_value',
            'missed-deduction-value': 'prompt_monetary_value_list',
            'third-party': 'prompt_third_party_bool',
            'third-party-given-name': 'prompt_third_party_name',
            'third-party-last-name': 'prompt_third_party_name',
            'phone-number': 'prompt_phone_number',
            'PIN': 'prompt_pin'
        }

        # Order in which demographics questions will be asked (based on whether the field is populated yet)
        self.demographics_question_order = ['given-name', 'last-name', 'age', 'occupation', 'street_address',
                                            'social_security',   'is-married', 'num-dependents', 'filing_status', 'blind',
                                            'dual_status_alien']

        # Order in which spouse questions will be asked (based on whether the field is populated yet)
        self.demographics_spouse_question_order = [ 'spouse-given-name', 'spouse-last-name', 'spouse-age','spouse-ssn',
                                                   'spouse-blind']

        # Order in which dependents questions will be asked (based on whether the field is populated yet)
        self.demographics_dependent_slots = [
            'dependent-given-name',
            'dependent-last-name',
            'dependent-age',
            'dependent-ssn',
            'dependent-relation',
            'dependent-citizenship'
        ]

        # Mapping to all the relevant dependents questions
        self.demographics_dependent_question = {
            'dependent-given-name': 'What is their first name?',
            'dependent-last-name': 'What is their last name?',
            'dependent-age': 'How old are they?',
            'dependent-ssn': "What is their social security number, ITIN or ATIN?",
            'dependent-relation': 'What is their relationship to you? e.g. "She is my daughter"',
            'dependent-citizenship': 'Is this dependent a U.S. citizen, national, or resident alien (yes or no)?'
        }

        # Dictionary that maps the dependent number to the corresponding word
        # i.e., If you claimed your son as your first dependent, then this dictionary will figure out that your
        # daughter is your "second" dependent and will insert the word "second" into the conversation
        self.nth = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
        }

        # Maps all relevant fields about income/finances to the questions that will fulfill them
        self.income_finances = {
            'wages': 'Please take out your W-2 form. What are your total wages, salaries, and tips '
                     'as indicated in Box 1?',
            'owns-business': 'Do you own a business?',
            'owns-stocks-bonds': 'Do you own any stocks or bonds?',
            'tax-exempt-interest': 'Please take out Form 1099-INT or Form 1099-OID. If you have Form 1099-INT, what is '
                                   'your tax-exempt stated interest shown in box 8? If you have Form 1099 OID, what is '
                                   'your tax-exempt OID bond in Box 2 and tax-exempt OID in Box 11? If you have '
                                   'received Form 1099-DIV, please also list the value in Box 11. If you received none '
                                   'of these forms, report 0.',
            'taxable-interest': 'What are your total taxable interest income from Forms 1099-INT and 1099-OID? If you '
                                'did not receive any of these forms, report 0.',
            'has-1099-R': 'Have you received 1099-R form(s) this year relating to pensions and annuities plans?',
            'pensions-and-annuities': 'What are your total pension or annuity payments from box 1 of these '
                                      '1099-R forms? Please list them.',
            'pensions-and-annuities-taxable': 'What are the taxable amounts of you pension or annuity payments as '
                                              'shown in your 1099-R forms? Please list them.',
            'has-1099-DIV': 'Did your bank or brokerage firm send you a 1099-DIV form?',
            'qualified-dividends':  'Looking at form 1099-DIV, what are your qualified dividends from field 1b?',
            'ordinary-dividends': 'Looking at form 1099-DIV, what are your ordinary dividends from field 1a?',
            'IRA-distributions': 'If you have an individual retirement account, or IRA, you will have form 1099-R. '
                                 'What are the gross distributions in box 1 of these forms? If you do not have an IRA, '
                                 'say zero.',
            'IRA-distributions-taxable': 'What is the taxable amount in box 2a of the 1099-R forms relating to IRAs?',
            'capital-gains': 'How much did you incur in capital gains or losses? (If you have filled out Schedule D '
                             'for capital gains, look at line 16).',
            'taxable-refunds': 'Please take out your Schedule 1 form, go to line 1. What is the amount of taxable '
                               'refunds or credits from this past year?',
            'business-income': 'Please go to line 3 of Schedule 1. How much money you have gained or lost from your'
                               ' business this past year? If you do not have a business, say zero.',
            'unemployment-compensation': 'Please go to line 7 of Schedule 1. How much did you collect in unemployment '
                                         'compensation this past year?',
            'other-income': 'Please go to line 8 of Schedule 1. What is the total amount you made or receieved in '
                            'forms of other income? Ignore the type.',
            'educator-expenses': 'What is your amount of educator expenses in line 10 of Schedule 1?',
            'business-expenses': 'What is your amount of business expenses in line 11 of Schedule 1?',
            'health-savings-deductions': 'What is your amount in health savings expenses in line 12 of Schedule 1?',
            'moving-expenses-armed-forces': 'What is your amount of moving expenses in line 13 of Schedule 1?',
            'self-employed-health-insurance': 'What is your amount in self employed health insurance in line 16 of '
                                              'Schedule 1?',
            'IRA-deductions': 'What is your amount in IRA deductions in line 19 of Schedule 1?',
            'student-loan-interest-deduction': 'What is your student loan interest deduction amount in line 20 of '
                                               'Schedule 1?',
            'tuition-fees': 'What is your amount of tuition and fees in line 21 of Schedule 1?',
            'federal-income-tax-withheld': 'What is your amount of federal income tax withheld from Forms W-2 and 1099?',
            'ss-benefits': 'Have you received Forms SSA-1099 and RRB-1099? If so, list the values in box 5 in each of '
                           'the forms. If not, say 0.',
            'schedule-2-line-3': 'Now, just a few more questions to go! Please have your Schedule 2 and 3 forms in '
                                 'front of you. What is your additional tax as stated in line 3 of Schedule 2?',
            'schedule-3-line-7': 'What are your nonrefundable credits as specified on line 7 of Schedule 3?',
            'schedule-2-line-10': 'What are your other taxes as indicated on line 10 of Schedule 2?',
            'schedule-3-line-14': 'What are your other payments and refundable credits as specified on line 14 of'
                                  ' Schedule 3?',
            'pass-through-business': "Do you own a pass-through-business (sole-proprietors and single-owner LLCs)? "
                                     "Is your income from the business taxed on your personal tax return?",
            'total-qualified-business-income': 'What is your total qualified income from your business?'
        }

        # Sets the order in which the income and finances questions will be asked
        self.income_finances_order = [
            'wages',
            'tax-exempt-interest',
            'taxable-interest',
            'has-1099-R',
            'pensions-and-annuities',
            'owns-business',
            'owns-stocks-bonds',
            'has-1099-DIV',
            'qualified-dividends',
            'ordinary-dividends',
            'IRA-distributions',
            'IRA-distributions-taxable',
            'ss-benefits',
            'capital-gains',
            'taxable-refunds',
            'business-income',
            'unemployment-compensation',
            'other-income',
            'educator-expenses',
            'business-expenses',
            'health-savings-deductions',
            'moving-expenses-armed-forces',
            'self-employed-health-insurance',
            'IRA-deductions',
            'student-loan-interest-deduction',
            'tuition-fees',
            'federal-income-tax-withheld',
            'earned-income-credit',
        ]

        # Mapping various stages of the deductions conversation to responses
        self.deductions = {
            # First question asked when transitioning to deductions section; allows user to claim deductions on their
            # own without needing help from us. This should help the user claim easy deductions up front and then the
            # agent needs to ask fewer questions later.
            'deduction-begin': "Let's figure out whether the standard or itemized deduction will save you more money. "
                               "First, do you have any deductions in mind that you might be eligible for?",

            # If the user right away does not have any deductions to claim themselves, they can go straight to
            # the agent asking them questions
            'user-done': 'Okay, now I am going to ask you a series of questions to get you maximum tax deductions!',

            # In the first deduction stage when the user is claiming deductions, if they mention something that
            # qualifies as a deduction, we let them know and they can continue claiming things or ask us for help.
            'deduction-success': 'Congrats, you saved yourself some money! What other deductions do you want to claim? '
                                 'If you want help from us, just say so!',

            # In the first deduction stage when the user is claiming deductions, if they mention something that does
            # not qualify as a deduction, we let them know and they can continue claiming things or ask us for help.
            'deduction-failure': 'Sorry, either that does not qualify for a deduction or we do not cover that '
                                 'deduction at this time. What other deductions you want to claim?'
                                 'If you want help from us, just say so!',

            # All the deductions covered so far by the agent (eight mentioned here plus tuition and student loans)
            'charitable-contribution': 'Have you donated any money to an American charity or non-profit? If so, what '
                                       'was the value of the donation? If not, say 0. Keep in mind that donating '
                                       'clothing, vehicles, or furniture in good condition can also count!',
            'state-local-taxes': 'What amount have you paid in state and local taxes?',
            'mortgage': 'What amount have you paid in home or condo mortgages?',
            'account_401': 'How much have you made in contributions to a 401K?',
            'roth-IRA': 'How much have you made in contributions to a Traditional IRA, if any?',
            'student-loans': 'How much did you repay in student loans?',
            'damaged-property': 'If you had any property damages in the last year, how much were your losses valued at?' 
                                ' To calculate this, subtract the value of your property after the incident from its '
                                'value before the incident. If no property has been damaged, say zero.',
            'medical-dental-expenses': 'How much have you paid in medical care, dental care, or '
                                       'pharmaceutical products?',
            'jury-duty': 'If you have served jury duty this year, how much were you paid? If you did not serve, say 0.'
        }

        # Corresponding questions for the refund section after the rest of the form has been filled out
        self.refund = {
            'amount-refunded': 'How much of that would you like refunded to you?',
            'overpaid-applied-tax': 'How much of the amount you overpaid would you like applied to your 2020 '
                                    'estimated tax?',
            'direct-deposit': 'Would you like this amount transferred to you through direct deposit?',
            'account-type': 'Is the account that you\'d like to deposit into a savings or checkings account?',
            'routing-number': 'What is your routing number?',
            'account-number': 'What is your account number?'
        }

        # Questions for filling out the third-party designee section
        self.third_party = {
            'third-party': 'Do you want to allow another person (other than your paid preparer) to discuss this return'
                           ' with the IRS?',
            'third-party-given-name': 'What is that person\'s name?',
            'third-party-last-name': 'What is that person\'s last name?',
            'phone-number': 'What is their phone number?',
            'PIN': 'What is their Personal Identification Number (PIN)?'
        }

    # Function that retrieves the next response from the Response class using its dictionaries, the current section
    # being filled out, and the next unfilled slot in the Document class
    def get_next_response(self, next_unfilled_slot, current_document):

        # If in the dependents section
        if current_document.dependent_being_filled is not None:
            return self.get_next_dependent_response(next_unfilled_slot,
                   current_document.demographic_user_info['num_dependents'], current_document.dependents)

        # If filling out spouse information
        if "spouse" in next_unfilled_slot:
            return self.demographics_spouse[next_unfilled_slot]

        # If trying to determine filing status in demographics
        elif "filing_status" in next_unfilled_slot:
            if current_document.is_married:
                return self.demographics['filing_status_married']
            elif not current_document.is_married and current_document.demographic_user_info['num_dependents'] == 0:
                current_document.demographic_user_info['filing_status'] = 'single'
                return "Your filing status is 'single.' " + self.demographics['dual_status_alien']
            else:
                return self.demographics['filing_status_HOH_widower']

        # Lets the user know what their filing status has been determined as; appends to next intended question
        elif next_unfilled_slot in self.demographics or next_unfilled_slot in self.demographics_dependent_slots:
            if next_unfilled_slot == 'dual_status_alien' and \
                    current_document.demographic_user_info['filing_status'] == 'married filing jointly':
                return "Your filing status is 'married filing jointly.' " + self.demographics['dual_status_alien']
            elif next_unfilled_slot == 'dual_status_alien' and \
                    current_document.demographic_user_info['filing_status'] == 'married filing separately':
                return "Your filing status is 'married filing separately.' " + self.demographics['dual_status_alien']
            elif next_unfilled_slot == 'dual_status_alien' and \
                    current_document.demographic_user_info['filing_status'] == 'qualifying widow':
                return "Your filing status is 'qualifying widow.' " + self.demographics['dual_status_alien']
            elif next_unfilled_slot == 'dual_status_alien' and \
                    current_document.demographic_user_info['filing_status'] == 'head of household':
                return "Your filing status is 'head of houshold.' " + self.demographics['dual_status_alien']
            return self.demographics[next_unfilled_slot]

        # Else try to find appropriate response from section that you are in
        elif next_unfilled_slot in self.income_finances:
            return self.income_finances[next_unfilled_slot]
        elif next_unfilled_slot in self.deductions:
            return self.deductions[next_unfilled_slot]
        elif next_unfilled_slot in self.refund:
            return self.get_next_refund_response(next_unfilled_slot, current_document)
        elif next_unfilled_slot in self.third_party:
            return self.third_party[next_unfilled_slot]
        return None

    # Generates responses during the dependents section and informs about their status for tax credits
    def get_next_dependent_response(self, next_unfilled_slot, dependent_num, dependents):
        if next_unfilled_slot == 'dependent-given-name':
            # Lets the user know about whether the previous dependent claimed qualified for a tax credit
            if dependent_num > 1:
                # Tax credit 1: Dependent child tax credit
                if dependents[dependent_num-2].dependent_child_tax_credit:
                    return dependents[dependent_num-2].slots['dependent-given-name'][0] + ' qualifies you for a child ' \
                           'tax credit. What is your ' + self.nth[dependent_num] + " dependent's full name, age, and " \
                           "relation to you?"

                # Tax credit 2: Dependent credit for others
                elif dependents[dependent_num-2].dependent_credit_for_others:
                    return dependents[dependent_num-2].slots['dependent-given-name'][0] +' qualifies you for a dependent' \
                            ' credit for others. What is your ' + self.nth[dependent_num] + " dependent's full name, " \
                            "age, and relation to you?"

                # Last dependent did not qualify for tax credit
                else:
                    return 'Unforunately, ' + dependents[dependent_num-2].slots['dependent-given-name'][0] +\
                           ' does not qualify you for a tax credit. What is your ' + self.nth[dependent_num] + \
                           " dependent's full name, age, and relation to you?"

            # For the first dependent being claimed
            else:
                return 'What is your ' + self.nth[dependent_num] + " dependent's full name, age, and relation to you?"
        else:   
            return self.demographics_dependent_question[next_unfilled_slot]

    # Uses the amount the user owes/is owed to generate the correct responses and directs the user to the
    # appropriate websites during this section
    def get_next_refund_response(self, next_unfilled_slot, document):
        if next_unfilled_slot == 'amount-refunded' and document.refund_user_info["overpaid"] > 0:
            return "The amount that you overpaid is ${}. How much of that would you like refunded to " \
                   "you?".format(document.refund_user_info["overpaid"])
        elif next_unfilled_slot == 'amount-refunded' and document.refund_user_info["overpaid"] <= 0:
            return "You owe ${}. To pay, please visit https://www.irs.gov/payments . We're done with your " \
                   "refund/owe section. Does everything look correct?".format(document.refund_user_info["amount-owed"])
        else:
            return self.refund[next_unfilled_slot]
        pass

    # Function that retrieves the next output contexts to improve the conversation flow in DialogFlow and prioritize
    # certain intent classifications
    def generate_output_context(self, slot, lifespan, session, current_document):

        # If the next unfilled slot is "filing status", this is a special case because the correct next question
        # and output context depends on whether the user is married and/or has dependents
        if slot == "filing_status":
            if current_document.is_married:
                context_identifier = session + "/contexts/" + 'prompt_filing_status_married'
            elif not current_document.is_married and current_document.demographic_user_info['num_dependents'] == 0:
                context_identifier = session + "/contexts/" + 'prompt_dual_status_alien'
            else:
                context_identifier = session + "/contexts/" + 'prompt_filing_status_widower'
        # If not filing status, generate the output context normally using the appropriate dictionary
        else:
            context_identifier = session + "/contexts/" + self.slot_to_output_contexts[slot]

        # Sets the output context correctly in the JSON object according to DialogFlow specifications
        context = [{
            "name": context_identifier,
            "lifespan_count": lifespan
        }, 
        {
            # We always include explain_term as an output context so the user can always prompt for a definition
            # at any time in the conversation
            "name": session + "/contexts/" + "explain_term",
            "lifespan_count": 1
        }]
        return context
