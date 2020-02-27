class Dependent:
    def __init__(self):
        self.slots = {
                    'given-name': None,
                    'last-name': None,
                    'age': None,
                    'social_security': None,
                    'relationship_to_filer': None,
                    #'dependent-child-tax-credit': [[False], False],
                    #'dependent-credit-for-others': [[False], False]
                    }
        self.num = 0

    def find_next_unfilled_slot(self):
        for slot, value, in self.slots.items():
            if value is None and value != '':
                return slot
        return None

    def update_slots(self, parameters, current_intent):
        for slot, value in self.slots.items():
            if value is None and slot in parameters and parameters[slot] is not '':
                self.slots[slot] = parameters[slot]