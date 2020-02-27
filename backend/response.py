class Response:
    def __init__(self):
        self.demographics = {'given-name': 'What is your given name?',
                        'last-name': 'What is your last name?',
                        'age': 'How old are you?',
                        'occupation': 'What is your occupation?',
                        'street-address': 'What is your full home address and ZIP code?',
                        'city': 'What city do you live in?',
                        'geo-country': 'What country do you live in?',
                        'geo-state': 'What state do you live in?',
                        'zip-code': "What's your ZIP code?",
                        'social_security': 'Please type in your social security number (SSN).',
                        'filing_status': 'What is your filing status?',
                        'dual_status_alien': "Are you a dual-status alien?",
                        'blind': "Are you blind?"
                        }

        self.demographics_spouse = {'spouse-given-name': "Since you're married, I will need some of your spouse's information. What is your spouse's name and age?",
                                    'spouse-last-name': "What is your spouse's last name?",
                                    'spouse-age': "What is your spouse's age?",
                                    'spouse-ssn': "Please type in your spouse's SSN.",
                                    'spouse-blind': 'Is your spouse blind?'}

        self.slot_to_output_contexts = { 'given-name': 'prompt_name',
                                         'last-name': 'prompt_name',
                                         'age': 'prompt_name',
                                         'occupation': 'prompt_name',
                                         'street-address': 'prompt_address',
                                         'geo-state': 'prompt_address',
                                         'city': 'prompt_address',
                                         'zip-code': 'prompt_address',
                                         'social_security': 'prompt_social_security',
                                         'filing_status': 'prompt_filing_status',
                                         'blind': 'prompt_blind',
                                         'dual_status_alien': "prompt_dual_status_alien",
                                         'spouse-given-name': "prompt_spouse_name_age",
                                         'spouse-last-name': "prompt_spouse_name_age",
                                         'spouse-age': "prompt_spouse_name_age",
                                         'spouse-ssn': "prompt_spouse_SSN",
                                         'spouse-blind': "prompt_spouse_blind"
                                         }

        self.demographics_question_order = ['given-name', 'last-name', 'age', 'occupation', 'street-address',
                                            'social_security', 'filing_status', 'blind', 'dual_status_alien']

        self.demographics_spouse_question_order = [  'spouse-given-name', 'spouse-last-name', 'spouse-age','spouse-ssn',
                                                   'spouse-blind']

        self.income_finances = {'wages': 'Now look at your W-2 form. What are your total wages, salaries, and tips?',
                                'capital-gains': 'Do you own any stocks or bonds?',
                                'owns-business': 'Do you own a business?',
                                'pensions-annuities': 'What are you pensions and annuities?',
                                'ss-benefits': 'How much have you claimed in social security this past year?',
                                'income-confirm': 'Please check the current income section. Are there any modifications you would like to make?',
                                'income-was-confirmed': "Great, we're almost done!"}

        self.income_finances_order = {'wages', 'capital_gains', 'owns-business', 'pensions-annuities', 'ss-benefits',
                                      'income-confirm', 'income-was-confirmed'}

    def get_next_response(self, next_unfilled_slot):
        if "spouse" in next_unfilled_slot:
            return self.demographics_spouse[next_unfilled_slot]
        elif next_unfilled_slot in self.demographics:
            return self.demographics[next_unfilled_slot]
        return None

    def generate_output_context(self, slot, lifespan, session):
        context_identifier = session + "/contexts/" + self.slot_to_output_contexts[slot]
        context = [{
            "name": context_identifier,
            "lifespan_count": lifespan
        }]
        return context