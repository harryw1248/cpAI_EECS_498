import json

class User:
    def __init__(self):
        self.demographics = {'given-name': '', 'last-name': '', 'street-address': '', 'city': '',
                             'state': '', 'zip-code': '', 'social_security': '', 'country': '', 'age': '',
                             'occupation': '', 'filing_status': ''}
        self.spouse_info = [[False, {'spouse-given-name': '', 'spouse-last-name': '', 'spouse-social_security': '',
                                     'mfs_spouse': '', 'spouse-blind': False}], False]
        self.income = {'wages': None, 'capital-gains': None, 'owns-business': None,
                       'pensions-annuities': None, 'ss-benefits': None}

        # the second False corresponds to whether or not the user has told you the information yet
        # i.e., self.PO = [[True], True] means the user told you they have a PO box while
        # self.PO  = [[False]], True] means the user has told you they don't have a PO box
        self.HOH_QW_child = ""
        self.PO = [[False], False]   # For now, don't specifically prompt user for this. He/she can modify on own
        self.apt_num = [[""], False]
        self.PES = [[False, False], False]
        self.is_foreign_address = [[False, False]]
        self.foreign_country_info = [["", "", ""], False]
        self.user_age_blind = [[False, False], False]
        self.spouse_age_blind = [[False, False], False]
        self.list_of_dependents = [[], False]
        self.uses_standardized_deductions = [[False], False]
        self.field_values = dict()

    def jsonify_user(self):
        user_dict = {}
        user_dict['first_name_middle_initial'] = self.demographics['given-name']
        user_dict['last_name'] = self.demographics['last-name']
        user_dict['social_security'] = self.demographics['social_security']
        user_dict['filing_status'] = self.demographics['filing_status']
        user_dict['mfs_spouse'] = self.spouse_info[0][1]['mfs_spouse']
        user_dict['HOH_QW_child'] = self.HOH_QW_child
        user_dict['has_spouse'] = self.spouse_info[0][0]
        user_dict['spouse_first_name_middle_initial'] = self.spouse_info[0][1]['mfs_spouse']
        user_dict['spouse_last_name'] = self.spouse_info[0][1]['spouse-last-name']
        user_dict['spouse_SSN'] = self.spouse_info[0][1]['spouse-social_security']
        user_dict['street-address'] = self.demographics['address']
        user_dict['city'] = self.demographics['city']
        user_dict['state'] = self.demographics['admin-area']
        user_dict['PO'] = self.PO[0][1]
        user_dict['apt_num'] = self.apt_num
        user_dict['PES'] = self.PES
        user_dict['is_foreign_address'] = self.is_foreign_address
        user_dict['foreign_country_info'] = self.foreign_country_info
        user_dict['standard_deduction_checkbox'] = self.uses_standardized_deductions
        user_dict['user_age_blind'] = self.user_age_blind
        user_dict['spouse_age_blind'] = self.spouse_age_blind
        user_dict['list_of_dependents'] = self.list_of_dependents
        user_dict['field_values'] = self.field_values
        return json.dumps(user_dict)

    def update_demographic_info(self, document):
        for slot in document.demographics_slots_to_fill:
            self.demographics[slot] = document.demographic_user_info[slot]

    def update_income_info(self, document):
        for slot in document.income_slots_to_fill:
            self.income[slot] = document.income_user_info[slot]

    def update_dummy(self):
        self.demographics["given-name"] = "Bob"
        self.demographics["last-name"] = "Jones"
        self.demographics["street-address"] = "64 Reinhart Street"
        self.demographics["city"] = "Oakland"
        self.demographics['state'] = "California"
        self.demographics['zip-code'] = "08894"
        self.demographics['social_security'] = "123456789"
        self.demographics['country'] = "USA"
        self.demographics["age"] = "67"
        self.demographics['occupation'] = "Plumber"
        self.demographics["filing_status"] = "Single"


        self.spouse_info = [[False, {'spouse-given-name': '', 'spouse-last-name': '', 'spouse-social_security': '',
                                     'mfs_spouse': '', 'spouse-blind': False}], True]

        self.HOH_QW_child = ""
        self.PO = [[False], True]   # For now, don't specifically prompt user for this. He/she can modify on own
        self.apt_num = [["3"], True]
        self.PES = [[False, False], True]
        self.is_foreign_address = [[False, False], True]
        self.foreign_country_info = [["", "", ""], True]
        self.user_age_blind = [[False, False], True]
        self.spouse_age_blind = [[False, False], True]
        self.list_of_dependents = [[], True]
        self.uses_standardized_deductions = [[True], True]
