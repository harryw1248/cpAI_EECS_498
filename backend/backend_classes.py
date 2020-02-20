class Document:
    def __init__(self):
        self.demographic_user_info = {'given-name': '',
                         'last-name': '',
                         'location': {
                             'admin-area': '',
                             'business-name': '',
                             'city': '',
                             'country': '',
                             'island': '',
                             'shortcut': '',
                             'street-address': '',
                             'subadmin-area': '',
                             'zip-code': ''
                         },
                         'social_security': '',
                         'filing_status': ''
                         }
        self.demographics_slots_to_fill = ['given-name', 'last-name', 'location', 'social_security', 'filing_status']
        self.ignore_location_info = {'business-name', 'island', 'shortcut', 'subadmin-area', 'country'}
        self.last_unfilled_field = ""

    def check_status(self, slot):
        if slot not in self.demographic_user_info:
            return "Error"
        elif slot == 'location':
            for key, value in self.demographic_user_info['location'].items():
                if value == '' and key not in self.ignore_location_info:
                    return key

            return None
        elif self.demographic_user_info[slot] == '':
            return slot
        else:
            return None

    def find_next_unfilled_slot_demographics(self):
        for slot in self.demographics_slots_to_fill:
            status = self.check_status(slot)
            if status is not None:
                return status

        return None

    def update_document_demographics(self, parameters):
        for slot, value in self.demographic_user_info.items():
            if slot == 'location':
                for location_key, location_value in self.demographic_user_info['location'].items():
                    if location_value == '' and parameters[slot] != '' and parameters[slot][location_key] != '':
                        self.demographic_user_info['location'][location_key] = parameters[slot][location_key]
            elif value == '' and slot in parameters and parameters[slot] != '':
                self.demographic_user_info[slot] = parameters[slot]


class Dependent:
    def __init__(self):
        self.info = {'dependent-name': '', 'dependent-SSN': '', 'dependent-relationship': '',
                     'dependent-child-tax-credit': [[False], False], 'depedent-credit-for-others': [[False], False]}


class User:
    def __init__(self):
        self.demographics = {'given-name': '', 'last-name': '', 'city': '', 'admin-area': '',
                             'street-address': '', 'zip-code': '', 'social_security': '', 'country': '', 'filing_status': -1}
        self.spouse_info = [[False, {'spouse-given-name': '', 'spouse-last-name': '', 'spouse-social_security': '',
                                     'mfs_spouse': ''}], False]

        self.HOH_QW_child = ""
        self.PO = [[False], False]
        self.apt_num = ["", False]
        self.PES = [[False, False], False]
        self.is_foreign_address = [[False, False]]
        self.foreign_country_info = [["", "", ""], False]
        self.more_than_four_dependents = [[False], False]
        self.standard_deduction_checkbox = [[], False]
        self.user_age_blind = [[False, False], False]
        self.spouse_age_blind = [[False, False], False]
        self.list_of_dependents = [[], False]
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
        user_dict['more_than_four_dependents'] = self.more_than_four_dependents
        user_dict['standard_deduction_checkbox'] = self.standard_deduction_checkbox
        user_dict['user_age_blind'] = self.user_age_blind
        user_dict['spouse_age_blind'] = self.spouse_age_blind
        user_dict['list_of_dependents'] = self.list_of_dependents
        user_dict['field_values'] = self.field_values
        return json.dumps(user_dict)

    def update_demographic_info(self, document):
        for slot in document.demographics_slots_to_fill:
            if slot is not 'location':
                self.demographics[slot] = document.demographic_user_info[slot]
            elif slot == 'location':
                location_vals = document.demographic_user_info['location']
                for inner_slot, inner_slot_val in location_vals.items():
                    if inner_slot in self.demographics:
                        self.demographics[inner_slot] = inner_slot_val


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