class Dependent:
    def __init__(self):
        self.slots = {
                    'dependent-given-name': None,
                    'dependent-last-name': None,
                    'dependent-age': None,
                    'dependent-ssn': None,
                    'dependent-relation': None,
                    'dependent-citizenship': None
                    }
        self.num = 0

        self.dependent_child_tax_credit = False
        self.dependent_credit_for_others = False

    def find_next_unfilled_slot(self):
        for slot, value, in self.slots.items():
            if value is None and value != '':
                return slot
        return None

    def determine_tax_credit(self):
        age_num = self.slots['dependent-age']
        print(self.slots['dependent-citizenship'])
        if self.slots['dependent-citizenship'] and age_num < 17:
            self.dependent_child_tax_credit = True
        elif self.slots['dependent-citizenship'] and age_num >= 17:
            self.dependent_credit_for_others = True
        else:
            return


    def update_slots(self, parameters, current_intent):
        for slot, value in self.slots.items():
            if value is None and slot in parameters and parameters[slot] is not '':
                if slot == 'dependent-citizenship':
                    print(parameters[slot])
                    if parameters[slot] == 'yes':
                        self.slots['dependent-citizenship'] = True
                    else:
                        self.slots['dependent-citizenship'] = False

                    self.determine_tax_credit()
                else:
                    self.slots[slot] = parameters[slot]