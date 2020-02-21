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
                         'filing_status': '',
                         'blind': '',
                         'dual_status_alien': ''
                         }
        self.demographics_slots_to_fill = ['given-name',
                                            'last-name',
                                            'location',
                                            'social_security',
                                            'filing_status',
                                            'dual_status_alien',
                                            'blind']
        self.bool_statuses = ['dual_status_alien',
                              'blind']

        self.ignore_location_info = {'business-name', 'island', 'shortcut', 'subadmin-area', 'country'}
        self.last_unfilled_field = ""
        self.last_intent = ""

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

    def update_document_demographics(self, parameters, current_intent):
        for slot, value in self.demographic_user_info.items():
            if 'location' in parameters and slot == 'location':
                for location_key, location_value in self.demographic_user_info['location'].items():
                    # There may be multiple location parameters per utterance
                    for location_object in parameters[slot]:
                        if location_value == '' and parameters[slot] != '' and location_object[location_key] != '':
                            self.demographic_user_info['location'][location_key] = location_object[location_key]
            elif value == '' and slot in parameters and parameters[slot] != '':
                self.demographic_user_info[slot] = parameters[slot]

        for status in self.bool_statuses:
            if status in current_intent:
                self.demographic_user_info[status] = True if 'yes' in current_intent else False