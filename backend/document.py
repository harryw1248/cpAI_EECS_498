from dependent import Dependent
import pandas as pd
import xlrd


class Document:
    def __init__(self):
        self.sections = [
            'demographics',
            'income',
            'deductions',
            'refund',
            'third-party'
        ]

        self.demographic_user_info = {
            'given-name': None,
            'last-name': None,
            'age': None,
            'occupation': None,
            'street_address': None,
            'city': None,
            'state': None,
            'zip-code': None,
            'social_security': None,
            'email': None,
            'user-phone-number': None,
            'is-married': None,
            'num_dependents': None,
            'filing_status': None,
            'lived-apart': None,
            'blind': None,
            'dual_status_alien': None,
            'claim-you-dependent': None,
            'claim-spouse-dependent': None,
            'spouse-itemize-separate': None,
        }

        self.demographic_spouse_info = {
            'spouse-given-name': None,
            'spouse-last-name': None,
            'spouse-age': None,
            'spouse-occupation': None,
            'spouse-ssn': None,
            'spouse-blind': None
        }

        self.demographics_slots_to_fill = [
            'given-name',
            'last-name',
            'age',
            'occupation',
            'street_address',
            'city',
            'state',
            'zip-code',
            'social_security',
            'email',
            'user-phone-number',
            'is-married',
            'num_dependents',
            'filing_status',
            'lived-apart',
            'dual_status_alien',
            'blind',
            'claim-you-dependent',
            'claim-spouse-dependent',
            'spouse-itemize-separate',
        ]

        self.income_user_info = {
            'wages': None,
            'owns-business': None,
            'pass-through-business': None,
            'total-qualified-business-income': None,
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
            'student-loan-interest-deduction': None,
            'tuition-fees': None,
            'adjustments-to-income': 0,
            'adjusted-gross-income': None,
            'federal-income-tax-withheld': None,
            'earned-income-credit': None,
            'ss-benefits': None,
            'ss-benefits-taxable': None,
            'business-gains': None,
            'taxable-income': None,
            'schedule-2-line-3': None,
            'schedule-3-line-7': None,
            'schedule-2-line-10': None,
            'schedule-3-line-14': None,

            # purely computational fields
            '7b': 0,
            '8b': 0,
            '9': 0,
            '10': 0,
            '11a': 0,
            '11b': 0,
            '12a': 0,
            '12b': 0,
            '13a': 0,
            '13b': 0,
            '14': 0,
            '15': 0,
            '16': 0,
            '18d': 0,
            '18e': 0,
            '19': 0
        }

        self.income_slots_to_fill = [
            'wages',
            'owns-business',
            'pass-through-business',
            'total-qualified-business-income',
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
            # Additional income ENDS here

            # adjustments-to-income' STARTS here
            'educator-expenses',
            'business-expenses',
            'health-savings-deductions',
            'moving-expenses-armed-forces',
            'self-employed-health-insurance',
            # 'penalty-early-withdrawal-savings',
            'IRA-deductions',
            'student-loan-interest-deduction',
            'tuition-fees',
            # 'adjustments-to-income' ENDS here,
            'ss-benefits',
            'federal-income-tax-withheld',
            'earned-income-credit',
            'schedule-2-line-3',
            'schedule-3-line-7',
            'schedule-2-line-10',
            'schedule-3-line-14'
        ]

        self.deduction_user_info = {
            'charitable-contribution': None,
            'state-local-taxes': None,
            'mortgage': None,
            'account_401': None,
            'roth-IRA': None,
            'medical-dental-expenses': None,
            'jury-duty': None,
            'damaged-property': None,
            'student-loan-interest': None,
            'tuition': None
        }

        self.deduction_slots_to_fill = [
            'charitable-contribution',
            'state-local-taxes',
            'mortgage',
            'account_401',
            'roth-IRA',
            'medical-dental-expenses',
            'jury-duty',
            'damaged-property'
        ]

        self.available_deductions = [
            'charitable-contribution',
            'state-local-taxes',
            'mortgage',
            'account_401',
            'roth-IRA',
            'medical-dental-expenses',
            'jury-duty',
            'damaged-property'
        ]

        self.refund_user_info = {
            'overpaid': None,
            'amount-refunded': None,
            'direct-deposit': None,
            'routing-number': None,
            'account-type': None,
            'account-number': None,
            'overpaid-applied-tax': None,
            'amount-owed': None,
            'estimated-tax-penalty': 0
        }

        self.refund_slots_to_fill = [
            'amount-refunded',
            'direct-deposit',
            'account-type',
            'routing-number',
            'account-number',
            'overpaid-applied-tax',
        ]

        self.third_party_user_info = {
            'third-party': None,
            'third-party-given-name': None,
            'third-party-last-name': None,
            'phone-number': None,
            'PIN': None
        }

        self.third_party_slots_to_fill = [
            'third-party',
            'third-party-given-name',
            'third-party-given-name',
            'phone-number',
            'PIN'
        ]

        self.dependent_being_filled = None
        self.number_of_dependents_completed = 0
        self.dependents = []
        self.demographics_slots_to_fill_if_married = ['spouse-given-name', 'spouse-last-name', 'spouse-age',
                                                      'spouse-ssn', 'spouse-blind']
        self.is_married = False
        self.current_section_index = 0
        self.last_unfilled_field = ""
        self.monetary_list_fields = ["wages", "tax-exempt-interest", "taxable-interest", "pensions-and-annuities",
                                     "pensions-and-annuities-taxable"]
        self.tax_amount = 0
        self.deduction_stage = 'deduction-begin'
        self.deduction_type_chosen = 'standard deduction'

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
        elif self.sections[self.current_section_index] == 'income':
            self.last_unfilled_field = self.find_next_unfilled_slot_income()
        elif self.sections[self.current_section_index] == 'deductions':
            self.last_unfilled_field = self.find_next_unfilled_slot_deductions()
        elif self.sections[self.current_section_index] == 'refund':
            self.last_unfilled_field = self.find_next_unfilled_slot_refund()
        elif self.sections[self.current_section_index] == 'third-party':
            self.last_unfilled_field = self.find_next_unfilled_slot_third_party()
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

    def find_next_unfilled_slot_deductions(self, deduction_result=None):
        if self.deduction_stage == 'deduction-begin':
            self.deduction_stage = 'user-enters-deductions'
            return 'deduction-begin'
        elif self.deduction_stage == 'user-enters-deductions' and deduction_result == 'deduction-success':
            return 'deduction-success'

        for slot in self.deduction_slots_to_fill:
            if self.deduction_user_info[slot] is None:
                return slot

        # self.income_user_info["9"] = self.compute_line_9()
        return None

    def find_next_unfilled_slot_refund(self):
        for slot in self.refund_slots_to_fill:
            if self.refund_user_info[slot] is None:
                return slot
        return None

    def find_next_unfilled_slot_third_party(self):
        for slot in self.third_party_slots_to_fill:
            if self.third_party_user_info[slot] is None:
                return slot
        return None

    def update_document_demographics(self, parameters, current_intent):
        # Check first if we're working on a dependent, because dependents are their own class
        if self.dependent_being_filled is not None:
            self.dependent_being_filled.update_slots(parameters, current_intent)
            return

        # Otherwise, fill out the corresponding dependent slot with the parameter value extracted from DF
        for slot, value in self.demographic_user_info.items():
            if value is None and slot in parameters and parameters[slot] != '':
                self.demographic_user_info[slot] = parameters[slot]

                if self.demographic_user_info["num_dependents"] is not None and \
                        self.demographic_user_info["num_dependents"] > 0:
                    self.demographic_user_info["claim-you-dependent"] = False

        # Make specific check for unemployment compensation after asking about occupation
        if 'name' in current_intent and "occupation" in parameters:
            if parameters['occupation'] != 'unemployed':
                self.income_user_info['unemployment-compensation'] = 0

        # Must handle bools differently (tech debt)
        elif current_intent == 'demographics_fill.blind_status':
            self.demographic_user_info['blind'] = True if parameters['blind'] == 'yes' else False

        elif current_intent == 'demographics_fill.dual_status_alien':
            self.demographic_user_info['dual_status_alien'] = True if parameters[
                                                                          'dual_status_alien'] == 'yes' else False

        elif "claim-you-dependent" in current_intent:
            if parameters['claim-you-dependent'] == 'yes':
                self.demographic_user_info['claim-you-dependent'] = True
            else:
                self.demographic_user_info['claim-you-dependent'] = False

        elif "claim-spouse-dependent" in current_intent:
            if parameters['claim-spouse-dependent'] == 'yes':
                self.demographic_user_info['claim-spouse-dependent'] = True
            else:
                self.demographic_user_info['claim-spouse-dependent'] = False

        elif "spouse-itemize-separate" in current_intent:
            if parameters['spouse-itemize-separate'] == 'yes':
                self.demographic_user_info['spouse-itemize-separate'] = True
            else:
                self.demographic_user_info['spouse-itemize-separate'] = False

        elif "is-married" in current_intent:
            if parameters['is-married'] == 'yes':
                self.is_married = True
            else:
                self.is_married = False
                self.demographic_user_info['lived-apart'] = True
                self.demographic_user_info['claim-spouse-dependent'] = False
                self.demographic_user_info['spouse-itemize-separate'] = False

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
                    if slot == "spouse-blind":
                        self.demographic_spouse_info[slot] = True if parameters[slot] == 'yes' else False

    def update_slot(self, parameters, current_intent, last_unfilled_field=None):
        if self.sections[self.current_section_index] == 'demographics':
            self.update_document_demographics(parameters, current_intent)

            extracted_slot_name = last_unfilled_field

            # Make assumptions about possible qualifying deductions based on age
            if "age" in parameters and self.demographic_user_info["age"] is not None:
                if self.demographic_user_info["age"] <= 22:
                    self.deduction_user_info['mortgage'] = 0
                if self.demographic_user_info["age"] <= 20:
                    self.deduction_user_info['account_401'] = 0
                if self.demographic_user_info["age"] >= 65:
                    self.deduction_user_info['jury-duty'] = 0

        elif self.sections[self.current_section_index] == 'income':
            # Note: this section is largely computational and mostly comes straight from the IRS instructions

            extracted_slot_name = last_unfilled_field

            # compute extracted slot value
            if current_intent == "income_and_finances_fill.monetary_value":
                if parameters['value'] != "":
                    extracted_slot_value = float(parameters['value'])
                elif parameters['dollar'] != "":
                    extracted_slot_value = float(parameters['dollar']["amount"])
                else:
                    extracted_slot_value = ""
            elif current_intent == "income_and_finances_fill.monetary_value_list":
                total = 0
                for value in parameters['value']:
                    total += value

                for value in parameters['dollar']:
                    total += value["amount"]
                extracted_slot_value = total
            elif 'gains_losses' in current_intent:
                if parameters['gain-or-loss'] == 'loss':
                    extracted_slot_value = parameters['value'] * -1
                else:
                    extracted_slot_value = parameters['value']
            else:
                try:
                    extracted_slot_value = parameters[extracted_slot_name]
                except:
                    extracted_slot_value = parameters['spouse-blind']


            # compute yes or no fields
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
                    self.income_user_info['business-income'] = 0
                    self.income_user_info['pass-through-business'] = False
                    self.income_user_info['total-qualified-business-income'] = False
                elif extracted_slot_name == 'pass-through-business':
                    self.income_user_info['total-qualified-business-income'] = 0
                # elif extracted_slot_name == 'owns-stocks-bonds':
                #     self.income_user_info['capital-gains'] = False
            elif extracted_slot_name == 'IRA-distributions' and extracted_slot_value == 'zero' or extracted_slot_value == '0' \
                    or extracted_slot_value == 0:
                self.income_user_info['IRA-distributions'] = 0
                self.income_user_info['IRA-distributions-taxable'] = 0
            elif extracted_slot_name == 'tuition-fees' or extracted_slot_name == 'IRA-deductions' or \
                    extracted_slot_name == 'IRA-deductions' or extracted_slot_name == 'self-employed-health-insurance' or \
                    extracted_slot_name == 'moving-expenses-armed-forces' or extracted_slot_name == 'health-savings-deductions' or \
                    extracted_slot_name == 'business-expenses' or extracted_slot_name == 'educator-expenses' or extracted_slot_name == 'student-loan-interest-deduction':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info['adjustments-to-income'] += extracted_slot_value
                if extracted_slot_name == 'student-loan-interest-deduction':
                    self.deduction_user_info['student-loan-interest'] = self.compute_student_loan_deduction(
                        extracted_slot_value)
                if extracted_slot_name == 'tuition-fees':
                    self.deduction_user_info['tuition'] = self.compute_tuition_deduction(extracted_slot_value)

            # compute all other income fields
            if extracted_slot_name == 'wages':
                if self.demographic_user_info['occupation'] != 'teacher' and self.demographic_user_info[
                    'occupation'] != 'educator':
                    self.income_user_info['educator-expenses'] = 0
            # if extracted_slot_name == 'tuition-fees':
            # self.income_user_info['earned-income-credit'] = self.compute_earned_income_credit()
            # ##DONT DELETE THE COMMENTED LINE BELOW
            # self.income_user_info["8b"] = self.income_user_info["7b"] - self.income_user_info["adjustments-to-income"]
            # self.income_user_info["adjusted-gross-income"] = self.income_user_info["7b"] - self.income_user_info["adjustments-to-income"]
            # self.compute_11a_and_11b()
            # self.income_user_info["12a"] = self.compute_tax_amount_12a()
            if extracted_slot_name in self.monetary_list_fields:
                self.income_user_info[extracted_slot_name] = extracted_slot_value
            elif extracted_slot_name == "ss-benefits":
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                final_value = self.compute_ss_benefits(extracted_slot_value)
                self.income_user_info['ss-benefits-taxable'] = final_value
                ##DONT DELETE THE COMMENTED LINE BELOW
                self.income_user_info["7b"] = self.compute_line_7b()
                self.income_user_info["total-income"] = self.compute_line_7b()
                self.income_user_info["8b"] = max(0, self.income_user_info["7b"] - self.income_user_info[
                    "adjustments-to-income"])
                self.income_user_info["adjusted-gross-income"] = max(0, self.income_user_info["7b"] -
                                                                     self.income_user_info[
                                                                         "adjustments-to-income"])
                self.income_user_info["9"] = self.compute_standard_deductions()
                self.compute_11a_and_11b()
                self.income_user_info["12a"] = self.compute_tax_amount_12a()
                self.income_user_info['earned-income-credit'] = self.compute_earned_income_credit()
            
            elif extracted_slot_name == 'total-qualified-business-income':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info['10'] = 0.20 * extracted_slot_value

            elif extracted_slot_name == 'other-income':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.compute_total_other_income()
            elif extracted_slot_name == 'schedule-2-line-3':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info["12b"] = extracted_slot_value + self.income_user_info["12a"]
            elif extracted_slot_name == 'schedule-3-line-7':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info["13a"] = self.set_line_13a()
                self.income_user_info["13b"] = extracted_slot_value + self.income_user_info["13a"]
                self.income_user_info["14"] = max(0, self.income_user_info["12b"] - self.income_user_info["13b"])
            elif extracted_slot_name == 'schedule-2-line-10':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info["15"] = extracted_slot_value
                self.income_user_info["16"] = self.income_user_info["14"] + self.income_user_info["15"]
            elif extracted_slot_name == 'schedule-3-line-14':
                self.income_user_info[extracted_slot_name] = extracted_slot_value
                self.income_user_info["18d"] = extracted_slot_value
                self.income_user_info["18e"] = self.income_user_info['earned-income-credit'] + self.income_user_info[
                    "18d"]
                self.income_user_info["19"] = self.income_user_info['federal-income-tax-withheld'] + \
                                              self.income_user_info["18e"]

                # Determine overpaid information
                self.compute_overpaid_amount()
            elif extracted_slot_value != 'yes' and extracted_slot_value != 'no':
                self.income_user_info[extracted_slot_name] = extracted_slot_value

        elif self.sections[self.current_section_index] == 'deductions':
            (deduction_name, dollar_values) = parameters
            print("DEDUCTIONS", parameters)
            print(deduction_name, dollar_values)
            if self.deduction_user_info[deduction_name] is None:
                self.deduction_user_info[deduction_name] = 0
            for dollar_value in dollar_values:
                self.deduction_user_info[deduction_name] += dollar_value

        elif self.sections[self.current_section_index] == 'refund':
            extracted_slot_name = last_unfilled_field

            # For amount-refunded, 'routing-number', and 'account-number'
            if current_intent == 'refund_and_owe.number_value':
                # If they would like to get all of their money refunded, set value to amount overpaid
                if parameters["number"] == "all":
                    self.refund_user_info[extracted_slot_name] = self.refund_user_info["overpaid"]
                # If they would like no money refunded, ignore the option to direct-deposit
                elif parameters["number"] == 0 and extracted_slot_name == 'amount-refunded':
                    self.refund_user_info['amount-refunded'] = 0
                    self.refund_user_info['direct-deposit'] = False
                    self.refund_user_info['account-type'] = False
                    self.refund_user_info['routing-number'] = False
                    self.refund_user_info['account-number'] = False
                else:
                    self.refund_user_info[extracted_slot_name] = parameters['number']

            # Only slot for this intent is direct-deposit
            elif current_intent == 'refund_and_owe.bool':
                if parameters['bool'] == "yes":
                    self.refund_user_info[extracted_slot_name] = True

                # If they would not like a refund, ignore the option to direct-deposit
                else:
                    self.refund_user_info[extracted_slot_name] = False
                    self.refund_user_info["account-type"] = False
                    self.refund_user_info["routing-number"] = False
                    self.refund_user_info["account-number"] = False
            else:
                self.refund_user_info[extracted_slot_name] = parameters[extracted_slot_name]

        elif self.sections[self.current_section_index] == 'third-party':
            if current_intent == 'third_party.bool':
                if parameters["third-party"] == "yes":
                    self.third_party_user_info['third-party'] = True
                # If they would not like to allow a third-party to access the tax form, do not inquire about them
                else:
                    self.third_party_user_info['third-party'] = False
                    self.third_party_user_info['third-party-given-name'] = False
                    self.third_party_user_info['third-party-given-name'] = False
                    self.third_party_user_info['phone-number'] = False
                    self.third_party_user_info['PIN'] = False
            else:
                self.third_party_user_info[last_unfilled_field] = parameters[last_unfilled_field]

        print(self.income_user_info)
        print(self.deduction_user_info)
        return None

    def compute_overpaid_amount(self):
        # This information comes directly from the IRS instructions about refund/owe amounts
        overpaid = self.income_user_info["19"] - self.income_user_info["16"]
        if overpaid > 0:
            self.refund_user_info["overpaid"] = overpaid
            self.refund_user_info["amount-owed"] = 0
        else:
            self.refund_user_info["overpaid"] = 0
            self.refund_user_info["amount-refunded"] = 0
            self.refund_user_info["direct-deposit"] = False
            self.refund_user_info["routing-number"] = False
            self.refund_user_info["account-type"] = False
            self.refund_user_info["account-number"] = False
            self.refund_user_info["overpaid-applied-tax"] = 0
            self.refund_user_info["amount-owed"] = self.income_user_info["16"] - self.income_user_info["19"]

        # Make assumptions (for project scope's sake) that estimated-tax-penalty is 0
        self.refund_user_info["estimated-tax-penalty"] = 0

    def compute_dependents_worksheet_13a(self):
        num_dependents_under_17_citizens = 0
        num_dependents_under_17_non_citizens = 0
        for dependent in self.dependents:
            if dependent.slots['dependent-age'] < 17 and dependent.slots['dependent-citizenship']:
                num_dependents_under_17_citizens += 1
            elif dependent.slots['dependent-age'] < 17 and not dependent.slots['dependent-citizenship']:
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

        line9 = self.income_user_info['12b']
        line10 = 0
        if line9 == line10:
            return 0
        else:
            line11 = line9 - line10

        if line8 > line11:
            return max(line11, 0)
        else:
            return max(line8, 0)

    def set_line_13a(self):
        self.child_dependent_tax_credit = self.compute_dependents_worksheet_13a()
        return self.child_dependent_tax_credit

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

        if line_6 > line_5:
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
            if line_8 > line_7:
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
            elif self.demographic_user_info["filing_status"] is 'head of household' or self.demographic_user_info[
                "filing_status"] is 'qualifying widow':
                line_10 = 9000
            elif self.demographic_user_info["filing_status"] is 'married filing separately' and \
                    self.demographic_user_info["lived-apart"] == True:
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
        # # TODO: add ss-benefits
        # self.income_user_info['total-income'] = (
        #         self.income_user_info['wages'] +
        #         self.income_user_info['taxable-interest'] +
        #         self.income_user_info['ordinary-dividends'] +
        #         self.income_user_info['IRA-distributions-taxable'] +
        #         self.income_user_info['pensions-and-annuities-taxable'] +
        #         self.income_user_info['capital-gains'] +
        #         self.income_user_info['total-other-income']
        # )

    def compute_11a_and_11b(self):
        # Line 9: standard deduction or itemized deduction
        # TODO
        deduction = self.income_user_info["9"]
        qualified_business_income = self.income_user_info["10"]
        self.income_user_info["11a"] = deduction + qualified_business_income
        self.income_user_info["taxable-income"] = max(self.income_user_info[
                                                          "8b"] - self.income_user_info["11a"], 0)
        self.income_user_info["11b"] = max(self.income_user_info[
                                               "8b"] - self.income_user_info["11a"], 0)

    def compute_standard_deductions(self):
        total_check_boxes = (int(self.demographic_user_info["age"]) > 65 + self.demographic_user_info["blind"] == True +
                             self.demographic_spouse_info['spouse-age'] is not None and int(
                    self.demographic_spouse_info[
                        'spouse-age']) > 65 +
                             self.demographic_spouse_info['spouse-blind'] is not None and self.demographic_spouse_info[
                                 'spouse-blind'] == True)
        if self.demographic_user_info['claim-you-dependent'] == False and \
                self.demographic_user_info['claim-spouse-dependent'] == False and \
                self.demographic_user_info['claim-you-dependent'] == False and total_check_boxes == 0:

            if self.demographic_user_info["filing_status"] is "married filing jointly" or self.demographic_user_info[
                "filing_status"] is "qualifying widow":
                return 24400
            elif self.demographic_user_info["filing_status"] is "married filing separately" or \
                    self.demographic_user_info["filing_status"] is "single":
                return 12200
            else:
                return 18350
        else:
            if self.demographic_user_info['spouse-itemize-separate'] == True or self.demographic_user_info[
                "dual_status_alien"] == True:
                return 0
            else:
                # total_check_boxes = (
                #             self.demographic_user_info["age"] > 65 + self.demographic_user_info["blind"] == True +
                #             self.demographic_spouse_info['spouse-age'] is not None and self.demographic_spouse_info[
                #                 'spouse-age'] > 65 +
                #             self.demographic_spouse_info['spouse-blind'] is not None and self.demographic_spouse_info[
                #                 'spouse-blind'] == True)
                if self.demographic_user_info["claim-spouse-dependent"] == True or self.demographic_user_info[
                    'claim-you-dependent'] == True:
                    earned_income = self.income_user_info["wages"]
                    line_2 = 0
                    if earned_income > 750:
                        line_2 = earned_income + 350
                    else:
                        line_2 = 1000

                    if self.demographic_user_info["filing_status"] is "married filing separately" or \
                            self.demographic_user_info["filing_status"] is "single":
                        line_3 = 12200
                    elif self.demographic_user_info["filing_status"] is "married filing jointly" or \
                            self.demographic_user_info["filing_status"] is "qualifying widow":
                        line_3 = 24400
                    else:
                        line_3 = 18350

                    line_4a = min(line_2, line_3)

                    if self.demographic_user_info["age"] <= 65 and self.demographic_user_info["blind"] == False:
                        return line_4a
                    else:
                        line_4b = 0
                        if self.demographic_user_info["filing_status"] is "single" or self.demographic_user_info[
                            "filing_status"] is 'head of household':
                            line_4b = total_check_boxes * 1650
                        else:
                            line_4b = total_check_boxes * 1300
                        return line_4b + line_4a
                elif self.demographic_user_info["age"] > 65 or self.demographic_user_info["blind"] == True:
                    std_deductions = {}
                    if self.demographic_user_info["filing_status"] == "single":
                        std_deductions = {1: 13850, 2: 15500, 3: 0, 4: 0}
                    elif self.demographic_user_info["filing_status"] == "married filing jointly":
                        std_deductions = {1: 25700, 2: 27000, 3: 28300, 4: 29600}
                    elif self.demographic_user_info["filing_status"] == "qualifying widow":
                        std_deductions = {1: 25700, 2: 27000, 3: 0, 4: 0}
                    elif self.demographic_user_info["filing_status"] == "married filing separately":
                        std_deductions = {1: 13500, 2: 14800, 3: 16100, 4: 17400}
                    else:
                        std_deductions = {1: 20000, 2: 21650, 3: 0, 4: 0}

                    return std_deductions[total_check_boxes]
                else:
                    return 0

    def compute_tax_amount_12a(self):
        taxable_income = self.income_user_info["taxable-income"]

        if taxable_income < 0:
            print("WARNING: TAXABLE INCOME IS NEGATIVE!!!")
            print("WARNING: TAXABLE INCOME IS NEGATIVE!!!")
            print("WARNING: TAXABLE INCOME IS NEGATIVE!!!")
            return 0
        elif taxable_income == 0:
            return 0
        filing_status = self.demographic_user_info["filing_status"]
        if taxable_income < 100000:
            data = pd.read_excel("tax_table.xlsx")
            tax_data = pd.DataFrame(data=data)
            for index, row in tax_data.iterrows():
                if taxable_income >= int(row['At Least']) and taxable_income < int(row['But Less Than']):
                    if filing_status is "married filing jointly" or filing_status is "qualifying widow":
                        self.tax_amount = int(row["married filing jointly"])
                    else:
                        self.tax_amount = int(row[filing_status])
        self.tax_amount = self.tax_computation_worksheet(taxable_income, filing_status)
        return self.tax_amount

    def compute_line_7b(self):
        # 1, 2b, 3b, 4b, 4d, 5b, 6, and 7a. T
        line_1 = self.income_user_info["wages"]
        line_2b = self.income_user_info["taxable-interest"]
        line_3b = self.income_user_info["ordinary-dividends"]
        line_4b = self.income_user_info["IRA-distributions-taxable"]
        line_4d = self.income_user_info["pensions-and-annuities-taxable"]
        line_5b = self.income_user_info["ss-benefits-taxable"]
        line_6 = self.income_user_info["capital-gains"]
        line_7a = self.income_user_info["total-other-income"]

        return line_1 + line_2b + line_3b + line_4b + line_4d + line_5b + line_6 + line_7a

    def compute_earned_income_credit(self):
        earned_income_credit = 0
        if self.demographic_user_info["filing_status"] is 'head of household' or \
                self.demographic_user_info["filing_status"] is 'qualifying widow' or \
                self.demographic_user_info["filing_status"] is 'single':

            if self.number_of_dependents_completed == 0:
                if self.income_user_info['adjusted-gross-income'] <= 15820:
                    earned_income_credit = 538
            if self.number_of_dependents_completed == 1:
                if self.income_user_info['adjusted-gross-income'] <= 41756:
                    earned_income_credit = 3584
            if self.number_of_dependents_completed == 2:
                if self.income_user_info['adjusted-gross-income'] <= 47440:
                    earned_income_credit = 5920
            if self.number_of_dependents_completed == 3:
                if self.income_user_info['adjusted-gross-income'] <= 50594:
                    earned_income_credit = 6660

        elif self.demographic_user_info["filing_status"] is 'married filing jointly':
            if self.number_of_dependents_completed == 0:
                if self.income_user_info['adjusted-gross-income'] <= 21710:
                    earned_income_credit = 538
            if self.number_of_dependents_completed == 1:
                if self.income_user_info['adjusted-gross-income'] <= 47646:
                    earned_income_credit = 3584
            if self.number_of_dependents_completed == 2:
                if self.income_user_info['adjusted-gross-income'] <= 53330:
                    earned_income_credit = 5920
            if self.number_of_dependents_completed == 3:
                if self.income_user_info['adjusted-gross-income'] <= 56844:
                    earned_income_credit = 6660

        if self.income_user_info['7b'] == 0:
            return 0
        if self.income_user_info['IRA-distributions'] <= 0:
            return 0
        if self.income_user_info['tax-exempt-interest'] == 0:
            return 0

        return earned_income_credit

    def compute_tuition_deduction(self, amount):
        if amount >= 4000:
            return 4000
        else:
            return amount

    def compute_student_loan_deduction(self, amount):
        if amount >= 2500:
            return 2500
        else:
            return amount

    def compute_line_9(self):
        # for key in self.deduction_user_info:
        #    if self.deduction_user_info[key] is None:
        #        self.deduction_user_info[key] = 0

        corrected_damaged_property = max(0, self.deduction_user_info['damaged-property'] - 100 - 0.10*self.income_user_info['adjusted-gross-income'])
        corrected_charitable_donations = min(0.50 * self.income_user_info['adjusted-gross-income'], self.deduction_user_info['charitable-contribution'])
        corrected_mortgage = min(self.deduction_user_info['mortgage'], 750000)
        corrected_ira = 0
        corrected_medical = max(0, self.deduction_user_info['medical-dental-expenses'] - 0.075 *self.income_user_info['adjusted-gross-income'])
        if int(self.demographic_user_info['age']) <= 49:
            corrected_ira = min(6000, self.deduction_user_info['roth-IRA'])
        else:
            corrected_ira = min(7000, self.deduction_user_info['roth-IRA'])

        corrected_student_loans = min(2500, self.deduction_user_info['student-loan-interest'])

        corrected_tuition = 0
        if self.income_user_info["wages"] <= 65000:
            corrected_ira = min(6000, self.deduction_user_info['tuition'])
        elif self.income_user_info["wages"] <= 80000:
            corrected_ira = min(2000, self.deduction_user_info['tuition'])

        corrected_state_local = min(10000, self.deduction_user_info['state-local-taxes'])

        print(self.deduction_user_info)
        itemized_deductions = corrected_charitable_donations + \
                              corrected_state_local + \
                              corrected_mortgage + \
                              corrected_ira + \
                              corrected_medical + \
                              self.deduction_user_info['jury-duty'] + \
                              corrected_student_loans + \
                              corrected_tuition + \
                              corrected_damaged_property

        print("standard_deductions: " + str(self.income_user_info["9"]))
        print("itemized_deductions: " + str(itemized_deductions))
        if self.income_user_info["9"] > itemized_deductions:
            return "standard deduction"
        else:
            self.income_user_info["9"] = itemized_deductions
            self.compute_11a_and_11b()
            self.income_user_info["12a"] = self.compute_tax_amount_12a()
            # self.income_user_info["12b"] = extracted_slot_value + self.income_user_info["12a"]
            self.income_user_info["12b"] = self.income_user_info["schedule-2-line-3"] + self.income_user_info["12a"]
            self.income_user_info["13a"] = self.set_line_13a()
            self.income_user_info["13b"] = self.income_user_info["schedule-3-line-7"] + self.income_user_info["13a"]
            self.income_user_info["14"] = max(0, self.income_user_info["12b"] - self.income_user_info["13b"])
            self.income_user_info["16"] = self.income_user_info["14"] + self.income_user_info["15"]
            return "itemized deduction"

    def update_dummy(self):
        self.demographic_user_info["given-name"] = "Bob"
        self.demographic_user_info["last-name"] = "Jones"
        self.demographic_user_info["street_address"] = "64 Reinhart Street"
        self.demographic_user_info["city"] = "Oakland"
        self.demographic_user_info['state'] = "California"
        self.demographic_user_info['zip-code'] = "08894"
        self.demographic_user_info['social_security'] = "123456789"
        self.demographic_user_info['country'] = "USA"
        self.demographic_user_info["age"] = "45"
        self.demographic_user_info['occupation'] = "Plumber"
        self.demographic_user_info["filing_status"] = "single"
        self.demographic_user_info["lived-apart"] = True

        self.demographic_user_info['claim-you-dependent'] = False
        self.demographic_user_info["claim-spouse-dependent"] = False
        self.demographic_user_info["spouse-itemize-separate"] = False
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

    def update_dummy2(self):
        self.demographic_user_info["age"] = "19"
        self.income_user_info['wages'] = 100000
        self.income_user_info['owns-business'] = False
        self.income_user_info['tax-exempt-interest'] = 1000
        self.income_user_info['taxable-interest'] = 50000
        self.income_user_info['has-1099-R'] = False
        self.income_user_info['pensions-and-annuities'] = 0
        self.income_user_info['pensions-and-annuities-taxable'] = 0
        self.income_user_info['owns-stocks-bonds'] = False
        self.income_user_info['has-1099-DIV'] = False
        self.income_user_info['qualified-dividends'] = 0
        self.income_user_info['ordinary-dividends'] = 0
        self.income_user_info['IRA-distributions'] = 0
        self.income_user_info['IRA-distributions-taxable'] = 0
        self.income_user_info['capital-gains'] = 0

        self.income_user_info['taxable-refunds'] = 0
        self.income_user_info['business-income'] = 0
        self.income_user_info['unemployment-compensation'] = 0
        self.income_user_info['other-income'] = 0
        self.income_user_info['total-other-income'] = 0
        self.income_user_info['total-income'] = 100000
        self.income_user_info['educator-expenses'] = 0
        self.income_user_info['business-expenses'] = 0
        self.income_user_info['health-savings-deductions'] = 0
        self.income_user_info['moving-expenses-armed-forces'] = 0
        self.income_user_info['self-employed-health-insurance'] = 0
        self.income_user_info['IRA-deductions'] = 0
        self.income_user_info['adjustments-to-income'] = 0
        self.income_user_info['adjusted-gross-income'] = 0
        self.income_user_info['federal-income-tax-withheld'] = 0
        self.income_user_info['earned-income-credit'] = 0
        self.income_user_info['ss-benefits'] = 0
        self.income_user_info['ss-benefits-taxable'] = 0
        self.income_user_info['business-gains'] = 0
        self.income_user_info['schedule-2-line-3'] = 0
        self.income_user_info['schedule-3-line-7'] = 0
        self.income_user_info['schedule-2-line-10'] = 0
        self.income_user_info['schedule-3-line-14'] = 0

        self.income_user_info['7b'] = 0
        self.income_user_info['8b'] = 0
        self.income_user_info['9'] = 1000
        self.income_user_info['10'] = 0
        self.income_user_info['11a'] = 0
        self.income_user_info['11b'] = 0
        self.income_user_info['12a'] = 0
        self.income_user_info['12b'] = 0
        self.income_user_info['13a'] = 0
        self.income_user_info['13b'] = 0
        self.income_user_info['14'] = 0
        self.income_user_info['15'] = 0
        self.income_user_info['16'] = 500
        self.income_user_info['18d'] = 0
        self.income_user_info['18e'] = 0
        self.income_user_info['19'] = 1500

        self.deduction_user_info['student-loan-interest'] = 0
        self.deduction_user_info['tuition'] = 0
        self.current_section_index = 2
        self.compute_overpaid_amount()

    def update_dummy3(self):
        self.current_section_index = 3