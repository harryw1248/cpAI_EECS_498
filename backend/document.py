from dependent import Dependent

class Document:
    def __init__(self):
        self.sections = [
            'demographics',
            'income'
        ]

        self.demographic_user_info = {  
            'given-name': None,
            'last-name': None,
            'age': None,
            'occupation': None,
            'street-address': None,
            'city': None,
            'state': None,
            'zip-code': None,
            'social_security': None,
            'is-married': None,
            'num_dependents': None,
            'filing_status': None,
            'blind': None,
            'dual_status_alien': None,
        }

        self.demographic_spouse_info = {    
            'spouse-given-name': None,
            'spouse-last-name': None,
            'spouse-age': None,
            'spouse-ssn': None,
            'spouse-blind': None
        }

        self.demographics_slots_to_fill = [ 
            'given-name',
            'last-name',
            'age',
            'occupation',
            'street-address',
            'city',
            'state',
            'zip-code',
            'social_security',
            'is-married',
            'num_dependents',
            'filing_status',
            'dual_status_alien',
            'blind',
        ]

        self.income_user_info = {
            'wages': None,
            'capital-gain': None
        }

        self.income_slots_to_fill = [
            'wages',
            'capital-gains',
        ]

        self.dependent_being_filled = None
        self.dependents = []
        self.demographics_slots_to_fill_if_married = ['spouse-given-name', 'spouse-last-name', 'spouse-age', 'spouse-ssn', 'spouse-blind']
        self.bool_statuses = ['dual_status_alien', 'blind']
        self.is_married = False
        self.current_section_index = 0

    def check_status(self, slot, slot_dictionary):
        if slot not in slot_dictionary:
            return "Error"
        elif slot_dictionary[slot] is None:
            return slot
        else:
            return None

    
    def find_next_unfilled_slot(self):
        if self.sections[self.current_section_index] == 'demographics':
            return self.find_next_unfilled_slot_demographics()
        elif self.sections[self.current_section_index] == 'income':
            return self.find_next_unfilled_slot_income()

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


    def find_next_unfilled_slot_income(self):
        for slot in self.income_slots_to_fill:
            if self.income_user_info[slot] is None:
                return slot
        return None


    def update_document_demographics(self, parameters, current_intent):
        # Check if we are currently working on a dependent
        # Beware of change_field!!!
        if self.dependent_being_filled is not None:
            self.dependent_being_filled.update_slots(parameters, current_intent)
            return

        for slot, value in self.demographic_user_info.items():
            if value is None and slot in parameters and parameters[slot] != '':
                self.demographic_user_info[slot] = parameters[slot]

        if "is-married" in current_intent:
            if parameters['is-married'] == 'yes':
                self.is_married = True
            else:
                self.is_married = False
        elif "filing_status_married" in current_intent:
            self.demographic_user_info['filing_status'] = parameters['filing-status-married']
        elif "widower" in current_intent:
            print(parameters['is-widower'])

            if parameters['is-widower'] == 'yes': # May need to slightly tweak in future to enforce dependent is CHILD
                self.demographic_user_info['filing_status'] = 'qualifying widow'
            else:
                self.demographic_user_info['filing_status'] = 'head of household'

        elif "spouse" in current_intent:
            for slot, value in self.demographic_spouse_info.items():
                if value is None and slot in parameters and parameters[slot] != '':
                    self.demographic_spouse_info[slot] = parameters[slot]

        for status in self.bool_statuses:
            if status in current_intent:
                self.demographic_user_info[status] = True if 'yes' in current_intent else False

        
    def update_slot(self, slot_name, new_slot_value):
        if self.sections[self.current_section_index] == 'demographics':
            self.demographic_user_info[slot_name] = new_slot_value
        elif self.sections[self.current_section_index] == 'income':
            pass

    