"""
Dependent.py
Class that houses the relevant information for dependents and computes the business logic that determines
    what tax credit a given dependent qualifies for, if any
Holds relevant demographic information for each dependent
In the Document class, a list is kept of each Dependent object
"""


class Dependent:
    def __init__(self):
        # Relevant demographic information; set to None initially to indicate that field has not been populated yet
        self.slots = {
            'dependent-given-name': None,
            'dependent-last-name': None,
            'dependent-age': None,
            'dependent-ssn': None,
            'dependent-relation': None,
            'dependent-citizenship': None
        }

        self.num = 0                                    # The dependent number (i.e., first, second, etc.)

        # Note: dependent can only qualify for one of the tax credits or none; cannot qualify for both
        self.dependent_child_tax_credit = False         # Set to True if this dependent qualifies for this tax credit
        self.dependent_credit_for_others = False        # Set to True if this dependent qualifies for this tax credit

    # Retrieves the next unfilled slot for this dependent
    def find_next_unfilled_slot(self):
        for slot, value, in self.slots.items():
            if value is None and value != '':
                return slot
        return None

    # Uses IRS guidelines to determine whether the dependent qualifies for a tax credit
    def determine_tax_credit(self):
        age_num = self.slots['dependent-age']
        if self.slots['dependent-citizenship'] and age_num < 17:
            self.dependent_child_tax_credit = True
        elif self.slots['dependent-citizenship'] and age_num >= 17:
            self.dependent_credit_for_others = True
        else:
            return

    # Updates the dependent information using extracted query information from DialogFlow
    def update_slots(self, parameters, current_intent):
        for slot, value in self.slots.items():
            if value is None and slot in parameters and parameters[slot] is not '':
                if slot == 'dependent-citizenship':
                    # Determines citizenship for dependent based on earlier question
                    if parameters[slot] == 'yes':
                        self.slots['dependent-citizenship'] = True
                    else:
                        self.slots['dependent-citizenship'] = False

                    # Now that citizenship is known, tax credit can be determined
                    self.determine_tax_credit()
                # Updates relevant parameters otherwise
                else:
                    self.slots[slot] = parameters[slot]
