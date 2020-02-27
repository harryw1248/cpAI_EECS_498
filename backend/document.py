from dependent import Dependent

class Document:
    def __init__(self):
        self.demographic_user_info = {  'given-name': None,
                                        'last-name': None,
                                        'age': None,
                                        'occupation': None,
                                        'street-address': None,
                                        'city': None,
                                        'state': None,
                                        'zip-code': None,
                                        'social_security': None,
                                        'filing_status': None,
                                        'blind': None,
                                        'dual_status_alien': None,
                                        'num_dependents': None,
                                    }

        self.demographic_spouse_info = {    'spouse-given-name': None,
                                            'spouse-last-name': None,
                                            'spouse-age': None,
                                            'spouse-ssn': None,
                                            'spouse-blind': None
                                        }

        self.demographics_slots_to_fill = [ 'given-name',
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
                                            'blind',
                                            'num_dependents',
                                            ]

        self.dependent_being_filled = None
        self.dependents = []
        self.demographics_slots_to_fill_if_married = ['spouse-given-name', 'spouse-last-name', 'spouse-age', 'spouse-ssn', 'spouse-blind']
        self.bool_statuses = ['dual_status_alien', 'blind']
        self.is_married = False

    def check_status(self, slot, slot_dictionary):
        if slot not in slot_dictionary:
            return "Error"
        elif slot_dictionary[slot] is None:
            return slot
        else:
            return None

    def find_next_unfilled_slot_demographics(self):
        # Get the next unfilled slot for the current dependent
        if self.dependent_being_filled is not None:
            slot = self.dependent_being_filled.find_next_unfilled_slot()
            if not slot:
                self.dependents.append(self.dependent_being_filled)
                self.dependent_being_filled = None
            else:
                return slot
        # Slots for user 
        for slot in self.demographics_slots_to_fill:
            status = self.check_status(slot, self.demographic_user_info)
            if status is not None:
                return status
        if self.is_married:
            for slot in self.demographics_slots_to_fill_if_married:
                status = self.check_status(slot, self.demographic_spouse_info)
                if status is not None:
                    return status
        if len(self.dependents) < self.demographic_user_info['num_dependents']:
            print("Creating a dependent!!")
            self.dependent_being_filled = Dependent()
            self.dependent_being_filled.num = len(self.dependents) + 1
            return self.dependent_being_filled.find_next_unfilled_slot()
        return None

    def update_document_demographics(self, parameters, current_intent):
        # Check if we are currently working on a dependent
        # Beware of change_field!!!
        if self.dependent_being_filled is not None:
            self.dependent_being_filled.update_slots(parameters, current_intent)
            return

        for slot, value in self.demographic_user_info.items():
            if value is None and slot in parameters and parameters[slot] is not '':
                self.demographic_user_info[slot] = parameters[slot]

        if "filing_status" in current_intent:
            if parameters['filing_status'] == 'married filing jointly' \
            or parameters['filing_status'] == 'married filing separately':
                self.is_married = True

        elif "spouse" in current_intent:
            for slot, value in self.demographic_spouse_info.items():
                if value is None and slot in parameters and parameters[slot] is not '':
                    self.demographic_spouse_info[slot] = parameters[slot]

        for status in self.bool_statuses:
            if status in current_intent:
                self.demographic_user_info[status] = True if 'yes' in current_intent else False