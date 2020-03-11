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
            # 'owns-business': None,
            'tax-exempt-interest': None,
            'taxable-interest': None, 
            'has-1099-R': None,
            'pensions-and-annuities': None, 
            'owns-stocks-bonds': None,
            'has-1099-DIV': None,
            'qualified-dividends': None,
            'ordinary-dividends': None,
            'IRA-distributions': None,
            'IRA-distributions-taxable': None,
            'capital-gains': None,
            'educator-expenses': None,
            'business-expenses': None,
            'health-savings-deductions': None,
            'moving-expenses-armed-forces': None,
            'self-employed-health-insurance': None,
            #'penalty-early-withdrawal-savings': None,
            'IRA-deductions': None,
            #'student-loan-interest-deduction': None,
            'tuition-fees': None,
            'adjustments-to-income': 0,
            'federal-income-tax-withheld': None,
            'earned-income-credit': None,
            'pensions-annuities': None,
            'ss-benefits': None
        }

        self.income_slots_to_fill = [
            'wages',
            # 'owns-business': None,
            'tax-exempt-interest',
            'taxable-interest', 
            'has-1099-R',
            'pensions-and-annuities', 
            'owns-stocks-bonds',
            'has-1099-DIV',
            'qualified-dividends',
            'ordinary-dividends',
            'IRA-distributions',
            'IRA-distributions-taxable',
            'capital-gains',
            'educator-expenses',
            'business-expenses',
            'health-savings-deductions',
            'moving-expenses-armed-forces',
            'self-employed-health-insurance',
            #'penalty-early-withdrawal-savings',
            'IRA-deductions',
            #'student-loan-interest-deduction',
            'tuition-fees',
            'adjustments-to-income',
            'federal-income-tax-withheld',
            'earned-income-credit',
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
                    if slot == 'spouse-blind':
                        self.demographic_spouse_info['spouse-blind'] = True if 'yes' in parameters[slot] else False

        for status in self.bool_statuses:
            if status in current_intent:
                self.demographic_user_info[status] = True if 'yes' in current_intent else False


    def update_slot(self, slot_name, new_slot_value):
        print(slot_name)
        print(new_slot_value)
        if self.sections[self.current_section_index] == 'demographics':

            if self.dependent_being_filled is not None and slot_name in self.dependent_being_filled.slots:
                self.dependent_being_filled.slots[slot_name] = new_slot_value

            elif slot_name in self.demographic_user_info:
                self.demographic_user_info[slot_name] = new_slot_value

            elif slot_name in self.demographic_spouse_info:
                self.demographic_spouse_info[slot_name] = new_slot_value
                if slot_name == 'spouse-blind':
                    self.demographic_spouse_info['spouse-blind'] = True if 'yes' in new_slot_value else False

        elif self.sections[self.current_section_index] == 'income':
            extracted_slot_name = list(slot_name.keys())[0]
            print(extracted_slot_name)
            extracted_slot_value = slot_name[extracted_slot_name]
            print(extracted_slot_value)

            if extracted_slot_value == 'yes':
                self.income_user_info[extracted_slot_name] = True
            elif extracted_slot_value == 'no':
                self.income_user_info[extracted_slot_name] = False
                if extracted_slot_name == 'has-1099-DIV' and not self.income_user_info['owns-stocks-bonds']:
                    self.income_user_info['ordinary-dividends'] = False
                    self.income_user_info['qualified-dividends'] = False
                    self.income_user_info['capital-gains'] = False
                elif extracted_slot_name == "has-1099-R":
                    self.income_user_info['pensions-and-annuities'] = 0
            elif extracted_slot_name == 'IRA-distributions' and extracted_slot_value == 'zero' or extracted_slot_value == '0'\
                    or extracted_slot_value == 0:
                self.income_user_info['IRA-distributions'] = 0
                self.income_user_info['IRA-distributions-taxable'] = 0
            elif extracted_slot_name == 'tuition-fees' or extracted_slot_name == 'IRA-deductions' or \
                    extracted_slot_name == 'IRA-deductions' or extracted_slot_name == 'self-employed-health-insurance' or \
                    extracted_slot_name == 'moving-expenses-armed-forces' or extracted_slot_name == 'health-savings-deductions' or \
                    extracted_slot_name == 'business-expenses' or extracted_slot_name == 'educator-expenses':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info['adjustments-to-income'] += extracted_slot_value
            elif extracted_slot_name == 'tax-exempt-interest':
                overall_sum = 0
                for val in extracted_slot_value:
                    overall_sum += val
                self.income_user_info[extracted_slot_name] = overall_sum
            else:
                self.income_user_info[extracted_slot_name] = extracted_slot_value

    def dependents_worksheet(self):
        num_dependents_under_17_citizens = 0
        num_dependents_under_17_non_citizens = 0
        for dependent in self.dependents:
            if dependent.slots['age'] < 17 and dependent.slots['dependent-citizenship']:
                num_dependents_under_17_citizens += 1
            elif dependent.slots['age'] < 17 and not dependent.slots['dependent-citizenship']:
                num_dependents_under_17_non_citizens += 1

        line3 = num_dependents_under_17_citizens * 2000.0 + num_dependents_under_17_non_citizens * 500.0
        line4 = self.income_user_info['adjusted-gross-income']
        if self.demographic_user_info['filing_status'] is 'married filing jointly':
            line5 = 400000.0
        else:
            line5 = 200000.0

        line7 = -1
        if line4 > line5:
            line6 = line4 - line5
            if line6 % 1000 is not 0:
                line6 = (int(line6/1000) + 1) * 1000.0
                line7 = 0.05 * line6
        else:
            line6 = 0
            line7 = 0

        if line3 > line7:
            line8 = line3 - line7
        else:
            return 0

        line9 = self.income_user_info['12b']
        line10 = 0
        if line9 == line10:
            return 0
        else:
            line11 = line9 - line10

        if line8 > line11:
            return line11
        else:
            return line8

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

