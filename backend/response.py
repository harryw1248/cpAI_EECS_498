class Response:
    def __init__(self):
        self.demographics = {'given-name': 'What is your given name?',
                        'last-name': 'What is your last name?',
                        'city': 'What city do you live in?',
                        'admin-area': 'What state you live in?',
                        'street-address': 'What is your street address?',
                        'zip-code': 'What is your zip code',
                        'social_security': 'What is your SSN?',
                        'filing_status': 'What is your filing status?'
                        }
        self.demographics_question_order = ['given-name', 'last-name', 'geo-city', 'geo-state', 'address',
                                            'zip-code', 'social_security', 'filing_status']