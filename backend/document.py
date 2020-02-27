class Document:
    def __init__(self):
        self.demographic_user_info = {  'given-name': '',
                                        'last-name': '',
                                        'age': '',
                                        'occupation': '',
                                        'street-address': '',
                                        'city': '',
                                        'state': '',
                                        'zip-code': '',
                                        'social_security': '',
                                        'filing_status': '',
                                        'blind': '',
                                        'dual_status_alien': ''
                                    }

        self.demographic_spouse_info = {'spouse-given-name': '', 'spouse-last-name': '', 'spouse-age': '',
                                        'spouse-ssn': '', 'spouse-blind': ''}

        self.demographics_slots_to_fill = ['given-name',
                                            'last-name',
                                           'age',
                                           'occupation',
                                            'street-address',
                                            'city',
                                            'state',
                                            'zip-code',
                                            'social_security',
                                            'filing_status',
                                            'dual_status_alien',
                                            'blind']

        self.demographics_slots_to_fill_if_married = ['spouse-given-name', 'spouse-last-name', 'spouse-age', 'spouse-ssn', 'spouse-blind']
        self.bool_statuses = ['dual_status_alien', 'blind']
        self.last_unfilled_field = ""
        self.last_intent = ""
        self.is_married = False

    def check_status(self, slot, slot_dictionary):
        if slot not in slot_dictionary:
            return "Error"
        elif slot_dictionary[slot] == '':
            return slot
        else:
            return None

    def find_next_unfilled_slot_demographics(self):
        for slot in self.demographics_slots_to_fill:
            status = self.check_status(slot, self.demographic_user_info)
            if status is not None:
                return status
        if self.is_married:
            for slot in self.demographics_slots_to_fill_if_married:
                status = self.check_status(slot, self.demographic_spouse_info)
                if status is not None:
                    return status
        return None

    def update_document_demographics(self, parameters, current_intent):
        for slot, value in self.demographic_user_info.items():
            if value == '' and slot in parameters and parameters[slot] != '':
                self.demographic_user_info[slot] = parameters[slot]

        if 'filing_status' in current_intent:
            if parameters['filing_status'] == 'married filing jointly' \
            or parameters['filing_status'] == 'married filing separately':
                self.is_married = True

        if "spouse" in current_intent:
            for slot, value in self.demographic_spouse_info.items():
                if value == '' and slot in parameters and parameters[slot] != '':
                    self.demographic_spouse_info[slot] = parameters[slot]

        for status in self.bool_statuses:
            if status in current_intent:
                self.demographic_user_info[status] = True if 'yes' in current_intent else False