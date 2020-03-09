class Response:
    def __init__(self):
        self.demographics = {
            'given-name': 'What is your first name?',
            'last-name': 'What is your last name?',
            'age': 'How old are you?',
            'occupation': 'What is your occupation? If you are retired, please say so.',
            'street-address': 'What is your full home address and ZIP code?',
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
            'blind': "Are you blind?"
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
            'street-address': 'prompt_address',
            'geo-state': 'prompt_address',
            'city': 'prompt_address',
            'zip-code': 'prompt_address',
            'social_security': 'prompt_social_security',
            'is-married': 'prompt_is_married',
            'dual_status_alien': "prompt_dual_status_alien",
            'blind': 'prompt_blind',
            'num_dependents': 'prompt_num_dependents',
            'dependent-citizenship': 'prompt_dependent_citizenship',
            'filing_status_married': 'prompt_filing_status_married',
            'filing_status_HOH_widower': 'prompt_filing_status_widower',
            'spouse-given-name': "prompt_spouse_name_age",
            'spouse-last-name': "prompt_spouse_name_age",
            'spouse-age': "prompt_spouse_name_age",
            'spouse-ssn': "prompt_spouse_SSN",
            'spouse-blind': "prompt_spouse_blind",
            'relationship_to_filer': "prompt_dependent_relation",
            'change_field_value': "prompt_change_field_value",
            'change_field_confirm': "prompt_change_field_confirm",
            'confirm_section': "prompt_confirm",
            'wages': "prompt_wages",
            'capital-gains': "prompt_capital_gains",
            'owns-business': 'prompt_owns_business',
            'owns-stocks-bonds': "prompt_stocks_bonds",
            'pensions-annuities': 'prompt_pensions_annuities',
            'ss-benefits': 'prompt_ss_benefits',
            'has-1099-DIV': 'prompt_has_1099_DIV',
            'qualified-dividends': 'prompt_qualified_dividends',
            'ordinary-dividends': 'prompt_ordinary_dividends',
            'IRA-distributions': 'prompt_IRA_distributions',
            'IRA-distributions-taxable': 'prompt_IRA_distributions_taxable'
        }

        self.demographics_question_order = ['given-name', 'last-name', 'age', 'occupation', 'street-address',
                                            'social_security',   'is-married', 'num-dependents', 'filing_status', 'blind',
                                            'dual_status_alien']

        self.demographics_spouse_question_order = [ 'spouse-given-name', 'spouse-last-name', 'spouse-age','spouse-ssn',
                                                   'spouse-blind']

        self.demographics_dependent_question = {
            'given-name': '',
            'last-name': 'What is their last name?',
            'age': 'How old are they?',
            'social_security': "What is their social security number, ITIN or ATIN?",
            'relationship_to_filer': 'What is their relationship to you? e.g. "She is my daughter"',
            'dependent-citizenship': 'Is this dependent a U.S. citizen, national, or resident alien?'
        }

        self.nth = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
        }

        self.income_finances = {
            'wages': 'Now look at your W-2 form. What are your total wages, salaries, and tips?',
            'owns-business': 'Do you own a business?',
            'owns-stocks-bonds': 'Do you own any stocks or bonds?',
            'has-1099-DIV': 'Did your bank or brokerage firm send you a 1099-DIV form?',
            'qualified-dividends':  'Looking at form 1099-DIV, what are your qualified dividends from field 1b?',
            'ordinary-dividends': 'Looking at form 1099-DIV, what are your ordinary dividends from field 1a?',
            'IRA-distributions': 'If you have an individual retirement account, or IRA, you will have form 1099-R. Please '
                                 'indicate the gross distributions in field 1. If you do not have an IRA, say zero.',
            'IRA-distributions-taxable': '. Please indicate the taxable amount in field 2a of form 1099-R.',
            'capital-gains': 'What is the amount of stocks or bonds you own?',
            'pensions-annuities': 'What is the amount of your pensions and annuities?',
            'ss-benefits': 'How much have you claimed in social security this past year?'
        }

        self.income_finances_order = [
            'wages',  'owns-business', 'owns-stocks-bonds', 'has-1099-DIV', 'qualified-dividends', 'ordinary-dividends',
            'IRA-distributions', 'IRA-distributions-taxable', 'capital-gains', 'pensions-annuities', 'ss-benefits'
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
        elif next_unfilled_slot in self.demographics:
            return self.demographics[next_unfilled_slot]
        elif next_unfilled_slot in self.income_finances:
            return self.income_finances[next_unfilled_slot]
        #print("couldn't find the response for slot:", next_unfilled_slot)
        return None

    def get_next_dependent_response(self, next_unfilled_slot, dependent_num, dependents):
        if next_unfilled_slot == 'given-name':
            if dependent_num > 1:
                if dependents[dependent_num-2].dependent_child_tax_credit:
                    return dependents[dependent_num-2].slots['given-name'] +' qualifies you for a child tax credit. ' \
                                                    'What is your ' + self.nth[dependent_num] + " dependent's full name?"
                elif dependents[dependent_num-2].dependent_credit_for_others:
                    return dependents[dependent_num-2].slots['given-name'] +' qualifies you for a dependent credit for others. ' \
                                                    'What is your ' + self.nth[dependent_num] + " dependent's full name?"
                else:
                    return 'Unforunately, ' + dependents[dependent_num-2].slots['given-name'] +' does not qualify you for a tax credit. ' \
                                                    'What is your ' + self.nth[dependent_num] + " dependent's full name?"
            else:
                return 'What is your ' + self.nth[dependent_num] + " dependent's full name?"
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
