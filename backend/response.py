class Response:
    def __init__(self):
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
            'is-married': 'Are you currently married?',
            'num_dependents': "How many dependents are you claiming?",
            'filing_status_married': 'Are you filing jointly with your spouse or filing separately?',
            'filing_status_HOH_widower': "Have you had a spouse die within the last two tax years?",
            'dual_status_alien': "Are you a dual-status alien?",
            'blind': "Are you blind?",
            'lived-apart': "Have you lived apart from your spouse for all of this year?"
        }

        self.demographics_spouse = {
            'spouse-given-name': "Since you're married, I will need some of your spouse's information. What is your spouse's name and age?",
            'spouse-last-name': "What is your spouse's last name?",
            'spouse-age': "What is your spouse's age?",
            'spouse-ssn': "Please type in your spouse's SSN.",
            'spouse-blind': 'Is your spouse blind?'
        }

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
            'spouse-ssn': "prompt_spouse_SSN",
            'spouse-blind': "prompt_spouse_blind",
            'dependent-given-name': "prompt_dependent_info",
            'dependent-last-name': "prompt_dependent_info",
            'dependent-age': "prompt_dependent_info",
            'dependent-relation': "prompt_dependent_info",
            'dependent-ssn': "prompt_dependent_ssn",
            'change_field_value': "prompt_change_field_value",
            'change_field_confirm': "prompt_change_field_confirm",
            'confirm_section': "prompt_confirm",
            'wages': "prompt_monetary_value",
            'tax-exempt-interest': 'prompt_monetary_value_list',
            'taxable-interest': 'prompt_monetary_value_list',
            'has-1099-R': 'prompt_has_1099_R',
            'pensions-and-annuities': 'prompt_monetary_value_list',
            'pensions-and-annuities-taxable': 'prompt_monetary_value_list',
            'capital-gains': "prompt_gains_losses",
            'taxable-refunds': "prompt_monetary_value",
            'business-income': "prompt_gains_losses",
            'unemployment-compensation':  'prompt_monetary_value',
            'other-income': 'prompt_monetary_value',
            'owns-business': 'prompt_owns_business',
            'owns-stocks-bonds': "prompt_stocks_bonds",
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
            #'penalty-early-withdrawal-savings': 'prompt_penalty_early_withdrawal_savings',
            'IRA-deductions': 'prompt_monetary_value',
            #'student-loan-interest-deduction': 'prompt_student_loan_interest_deduction',
            'tuition-fees': 'prompt_monetary_value',
            'federal-income-tax-withheld': 'prompt_monetary_value',
            'ss-benefits': 'prompt_monetary_value_list',
            'schedule-2-line-3': 'prompt_monetary_value',
            'schedule-3-line-7': 'prompt_monetary_value',
            'schedule-2-line-10': 'prompt_monetary_value',
            'schedule-3-line-14': 'prompt_monetary_value',
        }

        self.demographics_question_order = ['given-name', 'last-name', 'age', 'occupation', 'street_address',
                                            'social_security',   'is-married', 'num-dependents', 'filing_status', 'blind',
                                            'dual_status_alien']

        self.demographics_spouse_question_order = [ 'spouse-given-name', 'spouse-last-name', 'spouse-age','spouse-ssn',
                                                   'spouse-blind']

        self.demographics_dependent_slots = [
            'dependent-given-name',
            'dependent-last-name',
            'dependent-age',
            'dependent-ssn',
            'dependent-relation',
            'dependent-citizenship'
        ]

        self.demographics_dependent_question = {
            'dependent-given-name': 'What is their first name?',
            'dependent-last-name': 'What is their last name?',
            'dependent-age': 'How old are they?',
            'dependent-ssn': "What is their social security number, ITIN or ATIN?",
            'dependent-relation': 'What is their relationship to you? e.g. "She is my daughter"',
            'dependent-citizenship': 'Is this dependent a U.S. citizen, national, or resident alien (yes or no)?'
        }

        self.nth = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
        }

        self.income_finances = {
            'wages': 'Please take out your W-2 form. What are your total wages, salaries, and tips as indicated in Box 1?',
            'owns-business': 'Do you own a business?',
            'owns-stocks-bonds': 'Do you own any stocks or bonds?',
            'tax-exempt-interest': 'Please take out Form 1099-INT or Form 1099-OID. If you have Form 1099-INT, what is your your tax-exempt stated interest shown in box 8? If you '
                                    ' have Form 1099 OID, what is your tax-exempt OID bond in Box 2 and tax-exempt OID in Box 11? If you have received Form 1099-DIV, please also list '
                                    ' the value in Box 11. If you received none of these forms, report 0.',
            'taxable-interest': 'Please list your total taxable interest income from Forms 1099-INT and 1099-OID. If you did not recieve any of these forms, report 0.',
            'has-1099-R': 'Have you recieved 1099-R form(s) this year?',
            'pensions-and-annuities': 'What are your total pension or annuity payments from box 1 of your 1099-R forms? Please list them.',
            'pensions-and-annuities-taxable': 'What are the taxable amounts of you pension or annuity payments as shown in your 1099-R forms?. Please list them.',
            'has-1099-DIV': 'Did your bank or brokerage firm send you a 1099-DIV form?',
            'qualified-dividends':  'Looking at form 1099-DIV, what are your qualified dividends from field 1b?',
            'ordinary-dividends': 'Looking at form 1099-DIV, what are your ordinary dividends from field 1a?',
            'IRA-distributions': 'If you have an individual retirement account, or IRA, you will have form 1099-R. Please '
                                 'indicate the gross distributions in field 1. If you do not have an IRA, say zero.',
            'IRA-distributions-taxable': 'Please indicate the taxable amount in field 2a of form 1099-R.',
            'capital-gains': 'What is the amount of stocks or bonds you own?',
            'taxable-refunds': 'Please take out your Schedule 1 form, go to line 1, and read out the taxable refunds or credits.',
            'business-income': 'Please go to line 3 of Schedule 1 and read out how much money you gained or lost from your business. If you do not have a business, put zero.',
            'unemployment-compensation': 'Please go to line 7 of Schedule 1 and read out how much you collected in unemployment compensation.',
            'other-income': 'Please go to line 8 of Schedule 1 and read out the total you made or receieved in forms of other income. Ignore the type of income.',
            'educator-expenses': 'Please go to line 10 of Schedule 1 and read out how much you have in educator expenses.',
            'business-expenses': 'Please go to line 11 of Schedule 1 and read out how much you have in business expenses.',
            'health-savings-deductions': 'Please go to line 12 of Schedule 1 and read out how much you have in health savings expenses.',
            'moving-expenses-armed-forces': 'Please go to line 13 of Schedule 1 and read out how much you have in moving expenses.',
            'self-employed-health-insurance': 'Please go to line 16 of Schedule 1 and read out how much you have in self employed health insurance.',
            #'penalty-early-withdrawal-savings': 'What is your amount of penalty from early withdrawal from our savings?',
            'IRA-deductions': 'Please go to line 19 of Schedule 1 and read out how much you have in IRA deductions.',
            #'student-loan-interest-deduction': 'What is your student loan interest deduction amount?',
            'tuition-fees': 'Please go to line 21 of Schedule 1 and read out how much you have in tuition and fees.',
            'federal-income-tax-withheld': 'What is your amount of federal income tax withheld from Forms W-2 and 1099?',
            'ss-benefits': 'Have you recieved Forms SSA-1099 and RRB-1099? If so, list the values in box 5 in each of the forms. If not, say 0.',
            'schedule-2-line-3': 'Now, just a few more questions to go! Please have your Schedule 2 and 3 forms in front of you. What is your additional tax as stated in line 3 of Schedule 2?',
            'schedule-3-line-7': 'What are your nonrefundable credits as specified on line 7 of Schedule 3?',
            'schedule-2-line-10': 'What are your other taxes as indicated on line 10 of Schedule 2?',
            'schedule-3-line-14': 'What are your other payements and refundable credits as specified on line 14 of Schedule 3',   
        }

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
            #'penalty-early-withdrawal-savings',
            'IRA-deductions',
            #'student-loan-interest-deduction',
            'tuition-fees',
            'federal-income-tax-withheld',
            'earned-income-credit',
        ]


    #TODO: WAIT UNTIL WE GET INFORMATION ABOUT DEPENDENTS TO MAKE HOH OR QUALIFIED WIDOWER CLASSIFICATION
    # FOR NOW, WE ARE JUST USING UNMARRIED/DEPENDENT = HOH AND DEAD-SPOUSE/DEPEPDENT = QUALIFIED WIDOWER,
    # BUT WE CAN HOLD OFF ON MAKING THAT JUDGMENT IN THE BACKEND UNTIL WE GET MORE INFO ON DEPENDENT
    def get_next_response(self, next_unfilled_slot, current_document):
        #print("get_next_response called")
        if "spouse" in next_unfilled_slot:
            return self.demographics_spouse[next_unfilled_slot]
        elif "filing_status" in next_unfilled_slot:
            if current_document.is_married:
                return self.demographics['filing_status_married']
            elif not current_document.is_married and current_document.demographic_user_info['num_dependents'] == 0:
                current_document.demographic_user_info['filing_status'] = 'single'
                return "Your filing status is 'single.' " + self.demographics['dual_status_alien']
            else:
                return self.demographics['filing_status_HOH_widower']
        elif next_unfilled_slot in self.demographics or next_unfilled_slot in self.demographics_dependent_slots:
            if next_unfilled_slot == 'dual_status_alien' and current_document.demographic_user_info['filing_status'] == 'married filing jointly':
                return "Your filing status is 'married filing jointly.' " + self.demographics['dual_status_alien']
            elif next_unfilled_slot == 'dual_status_alien' and current_document.demographic_user_info['filing_status'] == 'married filing separately':
                return "Your filing status is 'married filing separately.' " + self.demographics['dual_status_alien']
            elif next_unfilled_slot == 'dual_status_alien' and current_document.demographic_user_info[
                'filing_status'] == 'qualifying widow':
                return "Your filing status is 'qualifying widow.' " + self.demographics['dual_status_alien']
            elif next_unfilled_slot == 'dual_status_alien' and current_document.demographic_user_info[
                'filing_status'] == 'head of household':
                return "Your filing status is 'head of houshold.' " + self.demographics['dual_status_alien']

            return self.demographics[next_unfilled_slot]
        elif next_unfilled_slot in self.income_finances:
            return self.income_finances[next_unfilled_slot]
        #print("couldn't find the response for slot:", next_unfilled_slot)
        return None

    def get_next_dependent_response(self, next_unfilled_slot, dependent_num, dependents):
        if next_unfilled_slot == 'dependent-given-name':
            if dependent_num > 1:
                if dependents[dependent_num-2].dependent_child_tax_credit:
                    return dependents[dependent_num-2].slots['dependent-given-name'] +' qualifies you for a child tax credit. ' \
                                                    'What is your ' + self.nth[dependent_num] + " dependent's full name, age, and relation to you?"
                elif dependents[dependent_num-2].dependent_credit_for_others:
                    return dependents[dependent_num-2].slots['dependent-given-name'] +' qualifies you for a dependent credit for others. ' \
                                                    'What is your ' + self.nth[dependent_num] + " dependent's full name, age, and relation to you?"
                else:
                    return 'Unforunately, ' + dependents[dependent_num-2].slots['dependent-given-name'] +' does not qualify you for a tax credit. ' \
                                                    'What is your ' + self.nth[dependent_num] + " dependent's full name, age, and relation to you?"
            else:
                return 'What is your ' + self.nth[dependent_num] + " dependent's full name, age, and relation to you?"
        else:   
            return self.demographics_dependent_question[next_unfilled_slot]

    def generate_output_context(self, slot, lifespan, session, current_document):
        #print("generate_output_context called")

        if slot == "filing_status":
            if current_document.is_married:
                context_identifier = session + "/contexts/" + 'prompt_filing_status_married'
            elif not current_document.is_married and current_document.demographic_user_info['num_dependents'] == 0:
                context_identifier = session + "/contexts/" + 'prompt_dual_status_alien'
            else:
                context_identifier = session + "/contexts/" + 'prompt_filing_status_widower'

        else:
            print("context: " + str(self.slot_to_output_contexts[slot]))
            context_identifier = session + "/contexts/" + self.slot_to_output_contexts[slot]

        context = [{
            "name": context_identifier,
            "lifespan_count": lifespan
        }]
        return context