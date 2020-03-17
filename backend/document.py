from dependent import Dependent
import pandas as pd
import xlrd

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
            'lived-apart': None,
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
            'lived-apart',
            'dual_status_alien',
            'blind',
        ]

        self.income_user_info = {
            'wages': None,
            'owns-business': None,
            'tax-exempt-interest': None,
            'taxable-interest': None,
            'has-1099-R': None,
            'pensions-and-annuities': None,
            'pensions-and-annuities-taxable': None,
            'owns-stocks-bonds': None,
            'has-1099-DIV': None,
            'qualified-dividends': None,
            'ordinary-dividends': None,
            'IRA-distributions': None,
            'IRA-distributions-taxable': None,
            'capital-gains': None,

            # additional income STARTS here
            'taxable-refunds': None,
            'business-income': None,
            'unemployment-compensation': None,
            'other-income': None,
            'total-other-income': None,
            'total-income': None,
            'educator-expenses': None,
            'business-expenses': None,
            'health-savings-deductions': None,
            'moving-expenses-armed-forces': None,
            'self-employed-health-insurance': None,
            # 'penalty-early-withdrawal-savings': None,
            'IRA-deductions': None,
            # 'student-loan-interest-deduction': None,
            'tuition-fees': None,
            'adjustments-to-income': 0,
            'adjusted-gross-income': None,
            'federal-income-tax-withheld': None,
            'earned-income-credit': None,
            'ss-benefits': None,
            'ss-benefits-taxable': None,
            'business-gains': None,
            '11a': None,
            'taxable-income': None
        }

        self.income_slots_to_fill = [
            'wages',
            'owns-business',
            'tax-exempt-interest',
            'taxable-interest',
            'owns-stocks-bonds',
            'has-1099-DIV',
            'qualified-dividends',
            'ordinary-dividends',
            'IRA-distributions',
            'IRA-distributions-taxable',
            'has-1099-R',
            'pensions-and-annuities',
            'pensions-and-annuities-taxable',
            'capital-gains',

            # Additional income STARTS here
            'taxable-refunds',
            'business-income',
            'unemployment-compensation',
            'other-income',

            # adjustments-to-income' STARTS here
            'educator-expenses',
            'business-expenses',
            'health-savings-deductions',
            'moving-expenses-armed-forces',
            'self-employed-health-insurance',
            # 'penalty-early-withdrawal-savings',
            'IRA-deductions',
            # 'student-loan-interest-deduction',
            'tuition-fees',
            # 'adjustments-to-income' ENDS here,
            'ss-benefits',

            'federal-income-tax-withheld',
            'earned-income-credit',
        ]

        self.dependent_being_filled = None
        self.number_of_dependents_completed = 0
        self.dependents = []
        self.demographics_slots_to_fill_if_married = ['spouse-given-name', 'spouse-last-name', 'spouse-age',
                                                      'spouse-ssn', 'spouse-blind']
        self.is_married = False
        self.current_section_index = 0
        self.last_unfilled_field = ""
        self.monetary_list_fields = ["tax-exempt-interest", "taxable-interest", "pensions-and-annuities",
                                     "pensions-and-annuities-taxable"]
        self.tax_amount = 0

    def check_status(self, slot, slot_dictionary):
        if slot not in slot_dictionary:
            return "Error"
        elif slot_dictionary[slot] is None:
            return slot
        else:
            return None

    def find_next_unfilled_slot(self):
        if self.sections[self.current_section_index] == 'demographics':
            self.last_unfilled_field = self.find_next_unfilled_slot_demographics()
            return self.last_unfilled_field
        elif self.sections[self.current_section_index] == 'income':
            self.last_unfilled_field = self.find_next_unfilled_slot_income()
            return self.last_unfilled_field

    def find_next_unfilled_slot_demographics(self):
        # Get the next unfilled slot for the current dependent
        if self.dependent_being_filled is not None:
            slot = self.dependent_being_filled.find_next_unfilled_slot()
            if not slot:
                self.number_of_dependents_completed += 1
                # self.dependents.append(self.dependent_being_filled)
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
        if self.number_of_dependents_completed < self.demographic_user_info['num_dependents']:
            print("Creating a dependent!!")
            self.dependent_being_filled = Dependent()
            self.dependent_being_filled.num = self.number_of_dependents_completed + 1
            self.dependents.append(self.dependent_being_filled)
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

        if current_intent == 'demographics_fill.name' and parameters['occupation'] != '':
            if parameters['occupation'] != 'unemployed':
                self.income_user_info['unemployment-compensation'] = 0
            if parameters['occupation'] != 'teacher' and parameters['occupation'] != 'educator':
                self.income_user_info['educator-expenses'] = 0
        elif current_intent == 'demographics_fill.blind_status':
            self.demographic_user_info['blind'] = True if parameters['blind'] == 'yes' else False
        elif current_intent == 'demographics_fill.dual_status_alien':
            self.demographic_user_info['dual_status_alien'] = True if parameters['dual_status_alien'] == 'yes' else False

        elif "is-married" in current_intent:
            if parameters['is-married'] == 'yes':
                self.is_married = True
            else:
                self.is_married = False
                self.demographic_user_info['lived-apart'] = True
        elif "filing_status_married" in current_intent:
            self.demographic_user_info['filing_status'] = parameters['filing-status-married']
        elif "widower" in current_intent:
            if parameters['is-widower'] == 'yes':  # May need to slightly tweak in future to enforce dependent is CHILD
                self.demographic_user_info['filing_status'] = 'qualifying widow'
            else:
                self.demographic_user_info['filing_status'] = 'head of household'

        elif "spouse" in current_intent:
            for slot, value in self.demographic_spouse_info.items():
                if value is None and slot in parameters and parameters[slot] != '':
                    self.demographic_spouse_info[slot] = parameters[slot]

    def update_slot(self, parameters, current_intent, last_unfilled_field=None):
        if self.sections[self.current_section_index] == 'demographics':
            self.update_document_demographics(parameters, current_intent)

        elif self.sections[self.current_section_index] == 'income':
            print("last unfilled field:", self.last_unfilled_field)
            extracted_slot_name = last_unfilled_field
            if current_intent == "income_and_finances_fill.monetary_value":
                extracted_slot_value = parameters['value']
            elif current_intent == "income_and_finances_fill.monetary_value_list":
                print("inside monetary value list")          
                total = 0
                for value in parameters['value']:
                    total += value
                extracted_slot_value = total
            elif 'gains_losses' in current_intent:
                if parameters['gain-or-loss'] == 'loss':
                    extracted_slot_value = parameters['value'] * -1
                else:
                    extracted_slot_value = parameters['value']
            else:
                extracted_slot_value = parameters[extracted_slot_name]
            print("extracted slot value is", extracted_slot_value)

            if extracted_slot_value == 'yes':
                self.income_user_info[extracted_slot_name] = True
            elif extracted_slot_value == 'no':
                self.income_user_info[extracted_slot_name] = False
                if extracted_slot_name == 'has-1099-DIV' and not self.income_user_info['owns-stocks-bonds']:
                    self.income_user_info['ordinary-dividends'] = False
                    self.income_user_info['qualified-dividends'] = False
                    self.income_user_info['capital-gains'] = False
                elif extracted_slot_name == 'has-1099-R':
                    self.income_user_info['pensions-and-annuities'] = 0
                    self.income_user_info['pensions-and-annuities-taxable'] = 0
                elif extracted_slot_name == 'owns-business':
                    self.income_user_info['business-expenses'] = 0
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
                self.income_user_info['adjusted-gross-income'] = self.income_user_info['adjustments-to-income'] - self.income_user_info['total-income']
            elif extracted_slot_name == 'tuition-fees' or extracted_slot_name == 'IRA-deductions' or \
                    extracted_slot_name == 'IRA-deductions' or extracted_slot_name == 'self-employed-health-insurance' or \
                    extracted_slot_name == 'moving-expenses-armed-forces' or extracted_slot_name == 'health-savings-deductions' or \
                    extracted_slot_name == 'business-expenses' or extracted_slot_name == 'educator-expenses':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info['adjustments-to-income'] += extracted_slot_value
                self.adjusted_gross_income = self.income_user_info['wages'] + self.income_user_info['adjustments-to-income']
                self.income_user_info['earned-income-credit'] = self.compute_earned_income_credit()
            elif extracted_slot_name in self.monetary_list_fields:
                overall_sum = 0
                for val in extracted_slot_value:
                    overall_sum += val
                self.income_user_info[extracted_slot_name] = overall_sum
                print("extracted slot name is", extracted_slot_name)
                print("updated tax-exempt-interest to be", self.income_user_info[extracted_slot_name])
            elif extracted_slot_name == "ss-benefits":
                overall_sum = 0
                for val in extracted_slot_value:
                    overall_sum += val

                self.income_user_info[extracted_slot_name] = overall_sum
                final_value = self.compute_ss_benefits(overall_sum)
                self.income_user_info['ss-benefits-taxable'] = final_value
            elif extracted_slot_name == 'other-income':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.compute_total_other_income()
            else:
                self.income_user_info[extracted_slot_name] = extracted_slot_value

    def compute_dependents_worksheet_13a(self):
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
                line6 = (int(line6 / 1000) + 1) * 1000.0
                line7 = 0.05 * line6
        else:
            line6 = 0
            line7 = 0

        if line3 > line7:
            line8 = line3 - line7
        else:
            return 0

        line9 = self.tax_amount
        line10 = 0
        if line9 == line10:
            return 0
        else:
            line11 = line9 - line10

        if line8 > line11:
            return line11
        else:
            return line8

    def set_line_13a(self):
        self.child_dependent_tax_credit = self.compute_dependents_worksheet_13a()

    def compute_ss_benefits(self, overall_sum=0):
        line_1 = overall_sum
        line_2 = 0.50 * line_1
        line_3 = (self.income_user_info["wages"] + self.income_user_info["taxable-interest"] +
                  self.income_user_info["ordinary-dividends"] + self.income_user_info["IRA-distributions-taxable"] +
                  self.income_user_info["pensions-and-annuities-taxable"])
        if self.income_user_info["capital-gains"] != None:
            line_3 += self.income_user_info["capital-gains"]

        line_4 = self.income_user_info["tax-exempt-interest"]
        line_5 = line_2 + line_3 + line_4
        line_6 = (self.income_user_info['educator-expenses'] +
                  self.income_user_info['business-expenses'] +
                  self.income_user_info['health-savings-deductions'] +
                  self.income_user_info['moving-expenses-armed-forces'] +
                  self.income_user_info['self-employed-health-insurance'] +
                  self.income_user_info['IRA-deductions'])

        if line_6 < line_5:
            return 0

        line_7 = line_5 - line_6
        line_8 = 0
        if self.demographic_user_info["filing_status"] is 'married filing jointly':
            line_8 = 32000
        elif self.demographic_user_info["filing_status"] is 'head of household' or self.demographic_user_info[
            "filing_status"] is 'qualifying widow':
            line_8 = 25000
        elif self.demographic_user_info["filing_status"] is 'married filing separately' and self.demographic_user_info[
            "lived-apart"] == True:
            line_8 = 25000
        else:
            line_8 = "skip"

        line_9, line_16 = 0, None
        if line_8 == "skip":
            line_16 = line_7 * 0.85
        else:
            if line_8 < line_7:
                return 0
            else:
                line_9 = line_7 - line_8

            line_10 = 0
            if self.demographic_user_info["filing_status"] is 'married filing jointly':
                line_10 = 12000
            elif self.demographic_user_info["filing_status"] is 'head of household' or self.demographic_user_info[
                "filing_status"] is 'qualifying widow':
                line_10 = 9000
            elif self.demographic_user_info["filing_status"] is 'married filing separately' and \
                    self.demographic_user_info["lived-apart"] == True:
                line_10 = 9000
            elif self.demographic_user_info["filing_status"] is 'head of household' or self.demographic_user_info["filing_status"] is 'qualifying widow':
                line_10 = 9000
            elif self.demographic_user_info["filing_status"] is 'married filing separately' and self.demographic_user_info["lived-apart"] == True:
                line_10 = 9000

            line_11 = max(0, line_9 - line_10)
            line_12 = min(line_9, line_10)
            line_13 = 0.5 * line_12
            line_14 = min(line_2, line_13)
            line_15 = line_11 * 0.85
            line_16 = line_14 + line_15

        line_17 = line_1 * 0.85
        line_18 = min(line_16, line_17)
        return line_18

    def tax_computation_worksheet(self, taxable_income, filing_status):
        data = pd.read_excel("tax_worksheet.xlsx")
        tax_data = pd.DataFrame(data=data)

        if filing_status == 'qualifying widow':
            filing_status = 'married filing jointly'

        for index, row in tax_data.iterrows():
            if int(row[filing_status + ' max']) == -1:
                mult_ = float(row[filing_status + ' multiplication'])
                subtraction_ = float(row[filing_status + ' subtraction'])
                return taxable_income * mult_ - subtraction_
            elif taxable_income >= int(row[filing_status + ' min']) and taxable_income < int(
                    row[filing_status + ' max']):
                mult_ = float(row[filing_status + ' multiplication'])
                subtraction_ = float(row[filing_status + ' subtraction'])
                return taxable_income * mult_ - subtraction_

    def compute_total_other_income(self):
        self.income_user_info["total-other-income"] = (
            self.income_user_info['taxable-refunds'] +
            self.income_user_info['business-income'] +
            self.income_user_info['unemployment-compensation'] + 
            self.income_user_info['other-income']
        )
        # TODO: add ss-benefits
        self.income_user_info['total-income'] = (
            self.income_user_info['wages'] + 
            self.income_user_info['taxable-interest'] + 
            self.income_user_info['ordinary-dividends'] + 
            self.income_user_info['IRA-distributions-taxable'] + 
            self.income_user_info['pensions-and-annuities-taxable'] + 
            self.income_user_info['capital-gains'] + 
            self.income_user_info['total-other-income']
        )

    def compute_11a_and_11b(self):
        # Line 9: standard deduction or itemized deduction
        # TODO
        deduction = 0
        # Line 10: Qualified business income deduction is assumed to be zero
        self.income_user_info["11a"] = deduction
        self.income_user_info["taxable-income"] = self.income_user_info["11a"] - self.income_user_info["adjustments-to-income"]

    def compute_tax_amount_12a(self, taxable_income, filing_status):
        taxable_income = self.income_user_info["taxable-income"]
        filing_status = self.demographic_user_info["filing_status"]
        if taxable_income < 100000:
            data = pd.read_excel("tax_table.xlsx")
            tax_data = pd.DataFrame(data=data)
            for index, row in tax_data.iterrows():
                if taxable_income >= int(row['At Least']) and taxable_income < int(row['But Less Than']):
                    if filing_status is "married filing jointly" or "qualifying widow":
                        self.tax_amount = int(row["married filing jointly"])
                    else:
                        self.tax_amount = int(row[filing_status])
        self.tax_amount =  self.tax_computation_worksheet(taxable_income, filing_status)
    
    def compute_earned_income_credit(self):
        earned_income_credit = 0
        if self.demographic_user_info["filing_status"] is 'head of household' or\
           self.demographic_user_info["filing_status"] is 'qualifying widow' or\
           self.demographic_user_info["filing_status"] is 'Single':

            if self.number_of_dependents_completed == 0:
                if self.adjusted_gross_income <= 15820:
                    earned_income_credit = 538
            if self.number_of_dependents_completed == 1:
                if self.adjusted_gross_income <= 41756:
                    earned_income_credit = 3584
            if self.number_of_dependents_completed == 2:
                if self.adjusted_gross_income <= 47440:
                    earned_income_credit = 5920
            if self.number_of_dependents_completed == 3:
                if self.adjusted_gross_income <= 50594:
                    earned_income_credit = 6660

        elif self.demographic_user_info["filing_status"] is 'married filing jointly':
            if self.number_of_dependents_completed == 0:
                if self.adjusted_gross_income <= 21710:
                    earned_income_credit = 538
            if self.number_of_dependents_completed == 1:
                if self.adjusted_gross_income <= 47646:
                    earned_income_credit = 3584
            if self.number_of_dependents_completed == 2:
                if self.adjusted_gross_income <= 53330:
                    earned_income_credit = 5920
            if self.number_of_dependents_completed == 3:
                if self.adjusted_gross_income <= 56844:
                    earned_income_credit = 6660
        print("earned income credit: " + str(earned_income_credit))
        return earned_income_credit

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
        self.demographic_user_info["lived-apart"] = True

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

        self.income_user_info['unemployment-compensation'] = 0

        self.current_section_index = 1