from dependent import Dependent

class Document:
    def __init__(self):
        self.sections = [
            'demographics',
            'income',
            'refund'
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
            'owns-business': None,
            'owns-stocks-bonds': None,
            'has-1099-DIV': None,
            'qualified-dividends': None,
            'ordinary-dividends': None,
            'IRA-distributions': None,
            'IRA-distributions-taxable': None,
            'capital-gains': None,
            'pensions-annuities': None,
            'ss-benefits': None
        }

        self.income_slots_to_fill = [
            'wages',
            'owns-business',
            'owns-stocks-bonds',
            'has-1099-DIV',
            'qualified-dividends',
            'ordinary-dividends',
            'IRA-distributions',
            'IRA-distributions-taxable',
            'capital-gains',
            'pensions-annuities',
            'ss-benefits',
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

            if self.dependent_being_filled is not None and slot_name in self.dependent_being_filled.slots:
                self.dependent_being_filled.slots[slot_name] = new_slot_value

            elif slot_name in self.demographic_user_info:
                self.demographic_user_info[slot_name] = new_slot_value

            elif slot_name in self.demographic_spouse_info:
                self.demographic_spouse_info[slot_name] = new_slot_value

        elif self.sections[self.current_section_index] == 'income':
            extracted_slot_name = list(slot_name.keys())[0]
            extracted_slot_value = slot_name[extracted_slot_name]

            if extracted_slot_value == 'yes':
                self.income_user_info[extracted_slot_name] = True
            elif extracted_slot_value == 'no':
                self.income_user_info[extracted_slot_name] = False
                if extracted_slot_name == 'has-1099-DIV' and not self.income_user_info['owns-stocks-bonds']:
                    self.income_user_info['ordinary-dividends'] = False
                    self.income_user_info['qualified-dividends'] = False
                    self.income_user_info['capital-gains'] = False
            elif extracted_slot_name == 'IRA-distributions' and extracted_slot_value == 'zero' or extracted_slot_value == '0'\
                    or extracted_slot_value == 0:
                self.income_user_info['IRA-distributions'] = 0
                self.income_user_info['IRA-distributions-taxable'] = 0
            else:
                self.income_user_info[extracted_slot_name] = extracted_slot_value

    def update_dummy(self):
        self.demographic_user_info["given-name"] = "Bob"
        self.demographic_user_info["last-name"] = "Jones"
        self.demographic_user_info["street-address"] = "64 Reinhart Street"
        self.demographic_user_info["city"] = "Oakland"
        self.demographic_user_info['state'] = "California"
        self.demographic_user_info['zip-code'] = "08894"
        self.demographic_user_info['social_security'] = "123456789"
        self.demographic_user_info['country'] = "USA"
        self.demographic_user_info["age"] = "67"
        self.demographic_user_info['occupation'] = "Plumber"
        self.demographic_user_info["filing_status"] = "Single"

        self.demographic_user_info["is-married"] = False
        
        self.demographic_user_info["num-dependents"] = 2
        self.demographic_user_info["blind"] = False

        self.demographic_user_info["dual_status_alien"] = False

        self.demographic_spouse_info = {
            'spouse-given-name': "Jane",
            'spouse-last-name': "Foster",
            'spouse-age': "56",
            'spouse-ssn': "123987654",
            'spouse-blind': False
        }

        self.current_section_index = 1