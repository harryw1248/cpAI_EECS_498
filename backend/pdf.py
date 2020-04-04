import os
import pdfrw
from pdf2image import convert_from_path
from PIL import Image

def nonePipe(val):
    if val is not None:
        return val
    return ''

def fillInFields(document):

    fields = {
        "þÿc1_01[0]": {'check': False}, # Single
        "þÿc1_01[1]": {'check': False}, # Married filing Jointly
        "þÿc1_01[2]": {'check': False}, # MFS
        "þÿc1_01[3]": {'check': False}, # HOH
        "þÿc1_01[4]": {'check': False}, # QW

        #"þÿf1_01[0]": {'V':""},
    
        # first/middlename,
        "þÿf1_02[0]": {'V': nonePipe(document.demographic_user_info['given-name'])},
        # last name
        "þÿf1_03[0]": {'V': nonePipe(document.demographic_user_info['last-name'])},
        # Your SSN
        "þÿf1_04[0]": {'V': nonePipe(document.demographic_user_info['social_security'])},

        # joint/spouse first/middle
        "þÿf1_05[0]": {'V': nonePipe(document.demographic_spouse_info['spouse-given-name'])},
        # joint/spouse last
        "þÿf1_06[0]": {'V': nonePipe(document.demographic_spouse_info['spouse-last-name'])},
        # joint/spouse SSN
        "þÿf1_07[0]": {'V': nonePipe(document.demographic_spouse_info['spouse-ssn'])},

        # Home Address
        "þÿf1_08[0]": {'V': nonePipe(document.demographic_user_info['street_address'])},
        # Apt Num
        "þÿf1_09[0]": {'V': ""},
        # City,town
        "þÿf1_10[0]": {'V': nonePipe(document.demographic_user_info['city']) + ' ' + nonePipe(document.demographic_user_info['state']) + ' ' + nonePipe(document.demographic_user_info['zip-code']) },
        # Foreign Country name
        "þÿf1_11[0]": {'V':""},
        # Foreign Province
        "þÿf1_12[0]": {'V':""},
        # Forieng postal
        "þÿf1_13[0]": {'V':""},
        "þÿc1_02[0]": {'check': False}, # Presidential Election Campaign You
        "þÿc1_03[0]": {'check': False}, # Presidential Election Campaign Spouse
        "þÿc1_04[0]": {'check': False}, # Standard Deduction Someone can claim You
        "þÿc1_05[0]": {'check': False}, # Standard Deduction Someone can claim Your Spouse
        "þÿc1_06[0]": {'check': False}, # Spouse itemizes..
        "þÿc1_07[0]": {'check': False}, # born before 1955
        "þÿc1_08[0]": {'check': document.demographic_user_info['blind']}, # Are blind
        "þÿc1_09[0]": {'check': False}, # Spouse before 1955
        "þÿc1_10[0]": {'check': document.demographic_spouse_info['spouse-blind']}, # is blind
        "þÿc1_11[0]": {'check': False}, # if more than four dependents
        "þÿf1_14[0]": {'V':""},
        "þÿf1_15[0]": {'V':""},
        "þÿf1_16[0]": {'V':""},
        "þÿc1_12[0]": {'check': False}, # child tax credit 1
        "þÿc1_13[0]": {'check': False}, # Credit for other dependents 1
        "þÿf1_17[0]": {'V':""},
        "þÿf1_18[0]": {'V':""},
        "þÿf1_19[0]": {'V':""},
        "þÿc1_14[0]": {'check': False},# child tax credit 2
        "þÿc1_15[0]": {'check': False},# Credit for other dependents 2
        "þÿf1_20[0]": {'V':""},
        "þÿf1_21[0]": {'V':""},
        "þÿf1_22[0]": {'V':""},
        "þÿc1_16[0]": {'check': False},# child tax credit 3
        "þÿc1_17[0]": {'check': False},# Credit for other dependents 3
        "þÿf1_23[0]": {'V':""},
        "þÿf1_24[0]": {'V':""},
        "þÿf1_25[0]": {'V':""},
        "þÿc1_18[0]": {'check': False},# child tax credit 4
        "þÿc1_19[0]": {'check': False},# Credit for other dependents 4
        "þÿf1_26[0]": {'V': nonePipe(document.income_user_info['wages'])}, #1 document.income_user_info
        "þÿf1_27[0]": {'V': nonePipe(document.income_user_info['tax-exempt-interest'])}, #2a
        "þÿf1_28[0]": {'V': nonePipe(document.income_user_info['taxable-interest'])}, #2b
        "þÿf1_29[0]": {'V': nonePipe(document.income_user_info['qualified-dividends'])}, #3a
        "þÿf1_30[0]": {'V': nonePipe(document.income_user_info['ordinary-dividends'])}, #3b
        "þÿf1_31[0]": {'V': nonePipe(document.income_user_info['IRA-distributions'])}, #4a
        "þÿf1_32[0]": {'V': nonePipe(document.income_user_info['IRA-distributions-taxable'])}, #4b
        "þÿf1_33[0]": {'V': nonePipe(document.income_user_info['pensions-and-annuities'])}, #4c
        "þÿf1_34[0]": {'V': nonePipe(document.income_user_info['pensions-and-annuities-taxable'])}, #4d
        "þÿf1_35[0]": {'V': nonePipe(document.income_user_info['ss-benefits'])}, #5a
        "þÿf1_36[0]": {'V': nonePipe(document.income_user_info['ss-benefits-taxable'])}, #5b
        "þÿc1_20[0]": {'check': False}, # 6 checkbox
        "þÿf1_37[0]": {'V': nonePipe(document.income_user_info['capital-gains'])}, #6
        "þÿf1_38[0]": {'V': nonePipe(document.income_user_info['other-income'])}, #7a
        "þÿf1_39[0]": {'V': document.income_user_info['7b']}, #7b
        "þÿf1_40[0]": {'V': document.income_user_info['adjustments-to-income']}, #8a
        "þÿf1_41[0]": {'V': document.income_user_info['8b']}, #8b
        "þÿf1_42[0]": {'V': ''}, #9
        "þÿf1_43[0]": {'V': ''}, #10
        "þÿf1_44[0]": {'V': document.income_user_info['11a']}, #11a
        "þÿf1_45[0]": {'V': document.income_user_info['11b']}, #11b
        "þÿc2_01[0]": {'check': False}, #12A checkbox1
        "þÿc2_02[0]": {'check': False}, #12A checkbox2
        "þÿc2_03[0]": {'check': False}, #12A checkbox3
        "þÿf2_01[0]": {'V': ''}, #12A checkbox input
        "þÿf2_02[0]": {'V': document.income_user_info['12a']}, #12a
        "þÿf2_03[0]": {'V': document.income_user_info['12b']}, #12b
        "þÿf2_04[0]": {'V': document.income_user_info['13a']}, #13a
        "þÿf2_05[0]": {'V': document.income_user_info['13b']}, #13b
        "þÿf2_06[0]": {'V': document.income_user_info['14']}, #14
        "þÿf2_07[0]": {'V': document.income_user_info['15']}, #15
        "þÿf2_08[0]": {'V': document.income_user_info['16']}, #16
        "þÿf2_09[0]": {'V': nonePipe(document.income_user_info['federal-income-tax-withheld'])}, #17
        "þÿf2_10[0]": {'V': nonePipe(document.income_user_info['earned-income-credit'])}, #18a
        "þÿf2_11[0]": {'V': ''}, #18b
        "þÿf2_12[0]": {'V': ''}, #18c
        "þÿf2_13[0]": {'V': document.income_user_info['18d']}, #18d
        "þÿf2_14[0]": {'V': document.income_user_info['18e']}, #18e
        "þÿf2_15[0]": {'V': document.income_user_info['19']}, #19

        # "þÿf2_16[0]":"",
        # "þÿc2_04[0]":"",
        # "þÿf2_17[0]":"",
        # "þÿf2_18[0]":"",
        # "þÿc2_05[0]":"",
        # "þÿc2_05[1]":"",
        # "þÿf2_19[0]":"",
        # "þÿf2_20[0]":"",
        # "þÿf2_21[0]":"",
        # "þÿf2_22[0]":"",
        # "þÿc2_06[0]":"",
        # "þÿc2_06[1]":"",
        # "þÿf2_23[0]":"",
        # "þÿf2_24[0]":"",
        # "þÿf2_25[0]":"",
        # "þÿf2_26[0]":"",
        # "þÿf2_27[0]":"",
        # "þÿf2_28[0]":"",
        # "þÿf2_29[0]":"",
        # "þÿf2_30[0]":"",
        # "þÿf2_31[0]":"",
        # "þÿf2_32[0]":"",
        # "þÿf2_33[0]":"",
        # "þÿc2_07[0]":"",
        # "þÿc2_07[1]":"",
        # "þÿf2_34[0]":"",
        # "þÿf2_35[0]":"",
        # "þÿf2_36[0]":"",
        # "þÿf2_37[0]":"",
    }

    if document.demographic_user_info['filing_status'] == "single":
        fields["þÿc1_01[0]"]['check'] = True
    elif document.demographic_user_info['filing_status'] == "married filing jointly": 
        fields["þÿc1_01[1]"]['check'] = True
    elif document.demographic_user_info['filing_status'] == "married filing separately":
        fields["þÿc1_01[2]"]['check'] = True
    elif document.demographic_user_info['filing_status'] == "head of household": 
        fields["þÿc1_01[3]"]['check'] = True
    elif document.demographic_user_info['filing_status'] == "qualifying widow":
        fields["þÿc1_01[4]"]['check'] = True

    if len(document.dependents) > 0:
        fields["þÿf1_14[0]"]['V'] = nonePipe(document.dependents[0].slots['dependent-given-name']) + '                                                      ' + nonePipe(document.dependents[0].slots['dependent-last-name'])
        fields["þÿf1_15[0]"]['V'] = nonePipe(document.dependents[0].slots['dependent-ssn'])
        fields["þÿf1_16[0]"]['V'] = nonePipe(document.dependents[0].slots['dependent-relation'])
        fields["þÿc1_12[0]"]['check'] = document.dependents[0].dependent_child_tax_credit     # child tax credit 1
        fields["þÿc1_13[0]"]['check'] = document.dependents[0].dependent_credit_for_others     # Credit for other dependents 1

    if len(document.dependents) > 1:
        fields["þÿf1_17[0]"]['V'] = nonePipe(document.dependents[1].slots['dependent-given-name'])  + '                                                      ' + nonePipe(document.dependents[1].slots['dependent-last-name'])
        fields["þÿf1_18[0]"]['V'] = nonePipe(document.dependents[1].slots['dependent-ssn'])
        fields["þÿf1_19[0]"]['V'] = nonePipe(document.dependents[1].slots['dependent-relation'] )
        fields["þÿc1_14[0]"]['check'] = document.dependents[1].dependent_child_tax_credit    # child tax credit 2
        fields["þÿc1_15[0]"]['check'] = document.dependents[1].dependent_credit_for_others    # Credit for other dependents 2

    if len(document.dependents) > 2:
        fields["þÿf1_20[0]"][''] = nonePipe(document.dependents[2].slots['dependent-given-name']) + '                                                      ' + nonePipe(document.dependents[2].slots['dependent-last-name'])
        fields["þÿf1_21[0]"][''] = nonePipe(document.dependents[2].slots['dependent-ssn'])
        fields["þÿf1_22[0]"][''] = nonePipe(document.dependents[2].slots['dependent-relation'])
        fields["þÿc1_16[0]"]['check'] = document.dependents[2].dependent_child_tax_credit    # child tax credit 3
        fields["þÿc1_17[0]"]['check'] = document.dependents[2].dependent_credit_for_others    # Credit for other dependents 3

    if len(document.dependents) > 3:
        fields["þÿf1_23[0]"][''] = nonePipe(document.dependents[3].slots['dependent-given-name']) + '                                                      ' + nonePipe(document.dependents[3].slots['dependent-last-name'])
        fields["þÿf1_24[0]"][''] = nonePipe(document.dependents[3].slots['dependent-ssn'])
        fields["þÿf1_25[0]"][''] = nonePipe(document.dependents[3].slots['dependent-relation'])
        fields["þÿc1_18[0]"]['check'] = document.dependents[3].dependent_child_tax_credit    # child tax credit 4
        fields["þÿc1_19[0]"]['check'] = document.dependents[3].dependent_credit_for_others   # Credit for other dependents 4

    return fields


def generatePdf(fields):
    ANNOT_KEY = '/Annots'
    ANNOT_FIELD_KEY = '/T'
    ANNOT_VAL_KEY = '/V'
    ANNOT_RECT_KEY = '/Rect'
    SUBTYPE_KEY = '/Subtype'
    WIDGET_SUBTYPE_KEY = '/Widget'

    template=pdfrw.PdfReader("f1040_template.pdf")
    for i in range(2):
        for annotation in template.pages[i][ANNOT_KEY]:
            if annotation[SUBTYPE_KEY] == WIDGET_SUBTYPE_KEY:
                if annotation[ANNOT_FIELD_KEY]:
                    key = str()
                    for each in annotation[ANNOT_FIELD_KEY][1:-1]:
                        if each != '\x00':
                            key = key + each
                    if key in fields.keys():
                        if 'check' in fields[key]:
                            if fields[key]['check']:
                                annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('On'), V=pdfrw.PdfName('On')))
                        else:
                            annotation.update(pdfrw.PdfDict(V='{}'.format(fields[key]['V'])))

    pdfrw.PdfWriter().write("./f1040.pdf", template)


def generateImage():
    pages = convert_from_path('./f1040.pdf', size=(900, None))
    pages[0].save('./page1.jpg', 'JPEG')
    pages[1].save('./page2.jpg', 'JPEG')


    page1 = Image.open('./page1.jpg')
    page2 = Image.open('./page2.jpg')

    combined = Image.new('RGB', (page1.width, int(page1.height*1.3)))
    combined.paste(page1, (0,-20))
    combined.paste(page2, (0, 740))
    combined.save('./page.jpg')