class Response:
    def __init__(self):
        self.demographics = {'given-name': 'What is your given name?',
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

        self.slot_to_output_contexts = { 'given-name': 'prompt_name',
                                         'last-name': 'prompt_name',
                                         'location': 'prompt_address',
                                         'admin-area': 'prompt_address',
                                         'city': 'prompt_address',
                                         'street-address': 'prompt_address',
                                         'zip-code': 'prompt_address',
                                         'social_security': 'prompt_social_security',
                                         'filing_status': 'prompt_filing_status',
                                         'blind': 'prompt_blind',
                                         'dual_status_alien': "prompt_dual_status_alien"}

        self.demographics_question_order = ['given-name', 'last-name', 'geo-city', 'geo-state', 'address',
                                            'zip-code', 'social_security', 'filing_status']

        self.income_finances = {'wages': 'Now look at your W-2 form. What are your total wages, salaries, and tips?',
                                'capital-gains': 'Do you own any stocks or bonds?',
                                'owns-business': 'Do you own a business?',
                                'pensions-annuities': 'What are you pensions and annuities?',
                                'ss-benefits': 'How much have you claimed in social security this past year?',
                                'income-confirm': 'Please check the current income section. Are there any modifications you would like to make?',
                                'income-was-confirmed': "Great, we're almost done!"}

        self.income_finances_order = {'wages', 'capital_gains', 'owns-business', 'pensions-annuities', 'ss-benefits',
                                      'income-confirm', 'income-was-confirmed'}

    def generate_output_context(self, slot, lifespan, session):
        print("slot:", slot)
        print("lifespan:", lifespan)
        print("session:", session)
        context_identifier = session + "/contexts/" + self.slot_to_output_contexts[slot]
        context = [{
            "name": context_identifier,
            "lifespan_count": lifespan
        }]
        return context