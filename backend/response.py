class Response:
    def __init__(self):
        self.demographics = {
            'given-name': 'What is your first name?',
            'last-name': 'What is your last name?',
            'age': 'How old are you?',
            'occupation': 'What is your occupation?',
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
            'filing_status': 'prompt_filing_status',
            'blind': 'prompt_blind',
            'dual_status_alien': "prompt_dual_status_alien",
            'num_dependents': 'prompt_num_dependents',
            'filing_status_married': 'prompt_filing_status_married',
            'filing_status_HOH_widower': 'prompt_filing_status',
            'spouse-given-name': "prompt_spouse_name_age",
            'spouse-last-name': "prompt_spouse_name_age",
            'spouse-age': "prompt_spouse_name_age",
            'spouse-ssn': "prompt_spouse_SSN",
            'spouse-blind': "prompt_spouse_blind",
            'relationship_to_filer': "prompt_dependent_relation"
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
            'social_security': "What is their social security number?",
            'relationship_to_filer': 'What is their relationship to you? e.g. "She is my daughter"'
        }

        self.nth = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
        }

        self.income_finances = {'wages': 'Now look at your W-2 form. What are your total wages, salaries, and tips?',
                                'capital-gains': 'Do you own any stocks or bonds?',
                                'owns-business': 'Do you own a business?',
                                'pensions-annuities': 'What are you pensions and annuities?',
                                'ss-benefits': 'How much have you claimed in social security this past year?',
                                'income-confirm': 'Please check the current income section. Are there any modifications you would like to make?',
                                'income-was-confirmed': "Great, we're almost done!"}

        self.income_finances_order = {'wages', 'capital_gains', 'owns-business', 'pensions-annuities', 'ss-benefits',
                                      'income-confirm', 'income-was-confirmed'}


    def get_next_response(self, next_unfilled_slot, current_document):
        if "spouse" in next_unfilled_slot:
            return self.demographics_spouse[next_unfilled_slot]
        elif "filing_status" in next_unfilled_slot:
            if current_document.is_married:
                return self.demographics['filing_status_married']
            elif not current_document.is_married and len(current_document.dependents) == 0:
                current_document.demographic_user_info['filing_status'] = 'single'
                return self.demographics['dual_status_alien']
            else:
                print("here")
                return self.demographics['filing_status_HOH_widower']
        elif next_unfilled_slot in self.demographics:
            return self.demographics[next_unfilled_slot]
        elif next_unfilled_slot in self.demographics_dependent_question:
            return self.demographics_dependent_question[next_unfilled_slot]
        return None

    def get_next_dependent_response(self, next_unfilled_slot, dependent_num):
        if next_unfilled_slot == 'given-name':
            return ('What is your ' + self.nth[dependent_num] + " dependent's full name and age?")
        else:   
            return self.demographics_dependent_question[next_unfilled_slot]

    def generate_output_context(self, slot, lifespan, session):
        print("inside generate_output_context")
        context_identifier = session + "/contexts/" + self.slot_to_output_contexts[slot]
        context = [{
            "name": context_identifier,
            "lifespan_count": lifespan
        }]
        return context