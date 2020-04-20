import os
import pdfrw
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import fitz
import datetime

def nonePipe(val):
    """Helper to output '' if val is None"""
    if val is not None:
        return val
    return ''


def fillInFields(document):
    """Map document object to the field names used in the pdf template for form 1040"""
    fields = {
        "þÿc1_01[0]": {'check': False}, # Single
        "þÿc1_01[1]": {'check': False}, # Married filing Jointly
        "þÿc1_01[2]": {'check': False}, # MFS
        "þÿc1_01[3]": {'check': False}, # HOH
        "þÿc1_01[4]": {'check': False}, # QW
    
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
        "þÿf1_39[0]": {'V': nonePipe(document.income_user_info['7b'])}, #7b
        "þÿf1_40[0]": {'V': nonePipe(document.income_user_info['adjustments-to-income'])}, #8a
        "þÿf1_41[0]": {'V': nonePipe(document.income_user_info['8b'])}, #8b
        "þÿf1_42[0]": {'V': nonePipe(document.income_user_info['9'])}, #9
        "þÿf1_43[0]": {'V': nonePipe(document.income_user_info['10'])}, #10
        "þÿf1_44[0]": {'V': nonePipe(document.income_user_info['11a'])}, #11a
        "þÿf1_45[0]": {'V': nonePipe(document.income_user_info['11b'])}, #11b
        "þÿc2_01[0]": {'check': False}, #12A checkbox1
        "þÿc2_02[0]": {'check': False}, #12A checkbox2
        "þÿc2_03[0]": {'check': False}, #12A checkbox3
        "þÿf2_01[0]": {'V': ''}, #12A checkbox input
        "þÿf2_02[0]": {'V': nonePipe(document.income_user_info['12a'])}, #12a
        "þÿf2_03[0]": {'V': nonePipe(document.income_user_info['12b'])}, #12b
        "þÿf2_04[0]": {'V': nonePipe(document.income_user_info['13a'])}, #13a
        "þÿf2_05[0]": {'V': nonePipe(document.income_user_info['13b'])}, #13b
        "þÿf2_06[0]": {'V': nonePipe(document.income_user_info['14'])}, #14
        "þÿf2_07[0]": {'V': nonePipe(document.income_user_info['15'])}, #15
        "þÿf2_08[0]": {'V': nonePipe(document.income_user_info['16'])}, #16
        "þÿf2_09[0]": {'V': nonePipe(document.income_user_info['federal-income-tax-withheld'])}, #17
        "þÿf2_10[0]": {'V': nonePipe(document.income_user_info['earned-income-credit'])}, #18a
        "þÿf2_11[0]": {'V': ''}, #18b
        "þÿf2_12[0]": {'V': ''}, #18c
        "þÿf2_13[0]": {'V': nonePipe(document.income_user_info['18d'])}, #18d
        "þÿf2_14[0]": {'V': nonePipe(document.income_user_info['18e'])}, #18e
        "þÿf2_15[0]": {'V': nonePipe(document.income_user_info['19'])}, #19


        "þÿf2_16[0]": {'V': nonePipe(document.refund_user_info['overpaid'])}, # 20
        "þÿc2_04[0]": {'check': False}, # 21a checkbox
        "þÿf2_17[0]": {'V': nonePipe(document.refund_user_info['amount-refunded'])}, # 21a
        "þÿf2_18[0]": {'V': nonePipe(document.refund_user_info['routing-number'])}, # Routing Num
        "þÿc2_05[0]": {'check': False}, # Checking Checkbox 
        "þÿc2_05[1]": {'check': False}, # Savings Checkbox
        "þÿf2_19[0]": {'V': nonePipe(document.refund_user_info['account-number'])}, # Account Number
        "þÿf2_20[0]": {'V': nonePipe(document.refund_user_info['overpaid-applied-tax'])}, # 22
        "þÿf2_21[0]": {'V': nonePipe(document.refund_user_info['amount-owed'])}, # 23
        "þÿf2_22[0]": {'V': nonePipe(document.refund_user_info['estimated-tax-penalty'])}, # 24

    
        "þÿc2_06[0]": {'check': False}, # Third party designee yes
        "þÿc2_06[1]": {'check': False}, # Third party designee no
        "þÿf2_23[0]": {'V': nonePipe(document.third_party_user_info['third-party-given-name'])
                             + ' '
                             + nonePipe(document.third_party_user_info['third-party-last-name'])}, # Designee's name
        "þÿf2_24[0]": {'V': nonePipe(document.third_party_user_info['phone-number'])}, # Phone No
        "þÿf2_25[0]": {'V': nonePipe(document.third_party_user_info['PIN'])}, # PIN
        
        # Your occupation
        "þÿf2_26[0]": {'V': nonePipe(document.demographic_user_info['occupation'])},
        # Identity Protection PIN for you
        "þÿf2_27[0]": {'V': ''},
        # Spouse's occupation
        "þÿf2_28[0]": {'V': nonePipe(document.demographic_spouse_info['spouse-occupation'])},
        # Identity Protection PIN for your spouse
        "þÿf2_29[0]": {'V': ''},
        # Phone no.
        "þÿf2_30[0]": {'V': ''},
        # Your email address
        "þÿf2_31[0]": {'V': ''},

        # Preparer's name
        "þÿf2_32[0]": {'V': 'cpAI'},
        # PTIN
        "þÿf2_33[0]": {'V': '1234'}, 
        "þÿc2_07[0]": {'check': False}, 
        "þÿc2_07[1]": {'check': False}, 
        # Firm's name
        "þÿf2_34[0]": {'V': 'cpAI'},
        # Phone no.
        "þÿf2_35[0]": {'V': '+1 800 123 1234'},
        # Firm's address
        "þÿf2_36[0]": {'V': '2281 Bonisteel Blvd MI 48104'},
        # Firm's EIN
        "þÿf2_37[0]": {'V': '123456789'},
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

    if len(document.dependents) > 0 and document.dependents[0].slots['dependent-given-name'] is not None and document.dependents[0].slots['dependent-last-name'] is not None: 
        fields["þÿf1_14[0]"]['V'] = nonePipe(document.dependents[0].slots['dependent-given-name'][0]) + ' ' +  nonePipe(document.dependents[0].slots['dependent-last-name'][0])
        fields["þÿf1_15[0]"]['V'] = nonePipe(document.dependents[0].slots['dependent-ssn'])
        fields["þÿf1_16[0]"]['V'] = nonePipe(document.dependents[0].slots['dependent-relation'])
        fields["þÿc1_12[0]"]['check'] = document.dependents[0].dependent_child_tax_credit     # child tax credit 1
        fields["þÿc1_13[0]"]['check'] = document.dependents[0].dependent_credit_for_others     # Credit for other dependents 1

    if len(document.dependents) > 1 and document.dependents[1].slots['dependent-given-name'] is not None and document.dependents[1].slots['dependent-last-name'] is not None:
        fields["þÿf1_17[0]"]['V'] = nonePipe(document.dependents[1].slots['dependent-given-name'][0])  + ' ' + nonePipe(document.dependents[1].slots['dependent-last-name'][0])
        fields["þÿf1_18[0]"]['V'] = nonePipe(document.dependents[1].slots['dependent-ssn'])
        fields["þÿf1_19[0]"]['V'] = nonePipe(document.dependents[1].slots['dependent-relation'] )
        fields["þÿc1_14[0]"]['check'] = document.dependents[1].dependent_child_tax_credit    # child tax credit 2
        fields["þÿc1_15[0]"]['check'] = document.dependents[1].dependent_credit_for_others    # Credit for other dependents 2

    if len(document.dependents) > 2 and document.dependents[2].slots['dependent-given-name'] is not None and document.dependents[2].slots['dependent-last-name'] is not None:
        fields["þÿf1_20[0]"][''] = nonePipe(document.dependents[2].slots['dependent-given-name'][0]) + '  ' + nonePipe(document.dependents[2].slots['dependent-last-name'])
        fields["þÿf1_21[0]"][''] = nonePipe(document.dependents[2].slots['dependent-ssn'])
        fields["þÿf1_22[0]"][''] = nonePipe(document.dependents[2].slots['dependent-relation'])
        fields["þÿc1_16[0]"]['check'] = document.dependents[2].dependent_child_tax_credit    # child tax credit 3
        fields["þÿc1_17[0]"]['check'] = document.dependents[2].dependent_credit_for_others    # Credit for other dependents 3

    if len(document.dependents) > 3 and document.dependents[3].slots['dependent-given-name'] is not None and document.dependents[3].slots['dependent-last-name'] is not None:
        fields["þÿf1_23[0]"][''] = nonePipe(document.dependents[3].slots['dependent-given-name'][0]) + ' ' + nonePipe(document.dependents[3].slots['dependent-last-name'][0])
        fields["þÿf1_24[0]"][''] = nonePipe(document.dependents[3].slots['dependent-ssn'])
        fields["þÿf1_25[0]"][''] = nonePipe(document.dependents[3].slots['dependent-relation'])
        fields["þÿc1_18[0]"]['check'] = document.dependents[3].dependent_child_tax_credit    # child tax credit 4
        fields["þÿc1_19[0]"]['check'] = document.dependents[3].dependent_credit_for_others   # Credit for other dependents 4

    if document.third_party_user_info['third-party'] is not None:
        fields["þÿc2_06[0]"]['check'] = document.third_party_user_info['third-party']
        fields["þÿc2_06[1]"]['check'] = not document.third_party_user_info['third-party']

    if document.refund_user_info['account-type'] is not None:
        if document.refund_user_info['account-type'] == 'checking':
            fields["þÿc2_05[0]"]['check'] = True
        if document.refund_user_info['account-type'] == 'savings': 
            fields["þÿc2_05[1]"]['check'] = True

    return fields


def generatePdf(fields, document):
    """Load the pdf template for form 1040 and write out the fields."""
    template=pdfrw.PdfReader("f1040_template.pdf")
    for i in range(2):
        for annotation in template.pages[i]['/Annots']:
            if annotation['/Subtype'] == '/Widget':
                if annotation['/T']:
                    key = str()
                    for each in annotation['/T'][1:-1]:
                        if each != '\x00':
                            key = key + each
                    if key in fields.keys():
                        if 'check' in fields[key]:
                            if fields[key]['check']:
                                annotation.update(pdfrw.PdfDict(AS=pdfrw.PdfName('On'), V=pdfrw.PdfName('On')))
                        else:
                            annotation.update(pdfrw.PdfDict(V='{}'.format(fields[key]['V'])))
    pdfrw.PdfWriter().write("./f1040.pdf", template)

    font = ImageFont.truetype('./dancing_script/static/DancingScript-Regular.ttf', size=20)
    image = Image.new(mode='RGB', size=(250, 25), color='rgb(255,255,255)')
    draw = ImageDraw.Draw(image)
    text = nonePipe(document.demographic_user_info['given-name']) + ' ' + nonePipe(document.demographic_user_info['last-name'])
    draw.text((5, 0), text, fill='rgb(0, 0, 0)', font=font)
    image.save('signature_user.png')
    image = Image.new(mode='RGB', size=(250, 25), color='rgb(255,255,255)')
    draw = ImageDraw.Draw(image)
    text = nonePipe(document.demographic_spouse_info['spouse-given-name']) + ' ' + nonePipe(document.demographic_spouse_info['spouse-last-name'])
    draw.text((5, 0), text, fill='rgb(0, 0, 0)', font=font)
    image.save('signature_spouse.png')
    image = Image.new(mode='RGB', size=(250, 25), color='rgb(255,255,255)')
    draw = ImageDraw.Draw(image)
    text = "cpai"
    draw.text((5, 0), text, fill='rgb(0, 0, 0)', font=font)
    image.save('signature_cpai.png')

    image = Image.new(mode='RGB', size=(100, 25), color='rgb(255,255,255)')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('./dancing_script/static/DancingScript-Regular.ttf', size=14)
    draw.text((5, 0), datetime.date.today().isoformat(), fill='rgb(0, 0, 0)', font=font)
    image.save('date.png')

    pos_user_sig = fitz.Rect(100, 375, 250, 400)
    pos_user_date = fitz.Rect(275, 375, 325, 400)
    pos_spouse_sig = fitz.Rect(100, 405, 250, 430)
    pos_spouse_date = fitz.Rect(275, 405, 325, 430)
    pos_cpai_sig = fitz.Rect(220, 448, 370, 460)
    pos_cpai_date = fitz.Rect(390, 440, 440, 470)

    pdf_file = fitz.open('./f1040.pdf')
    pdf_file[1].insertImage(pos_user_sig, filename="signature_user.png")
    pdf_file[1].insertImage(pos_spouse_sig, filename="signature_spouse.png")
    pdf_file[1].insertImage(pos_cpai_sig, filename="signature_cpai.png")
    pdf_file[1].insertImage(pos_user_date, filename="date.png")
    pdf_file[1].insertImage(pos_spouse_date, filename="date.png")
    pdf_file[1].insertImage(pos_cpai_date, filename="date.png")
    pdf_file.save('./f1040_signed.pdf')


def generateImage():
    """Generate a snapshot of the pdf generated by generatePdf()"""
    pages = convert_from_path('./f1040_signed.pdf', size=(900, None))
    pages[0].save('./page1.jpg', 'JPEG')
    pages[1].save('./page2.jpg', 'JPEG')


    page1 = Image.open('./page1.jpg')
    page2 = Image.open('./page2.jpg')

    combined = Image.new('RGB', (page1.width, int(page1.height*1.3)))
    combined.paste(page1, (0,-20))
    combined.paste(page2, (0, 740))
    combined.save('./page.jpg')