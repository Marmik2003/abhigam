from django import template
from datetime import datetime
import dateutil.parser
from ..models import ADMIT_PATIENT, PATIENT_DAILY_EXPENSE, PATIENT_DEPOSIT, ROOM_TYPE

register = template.Library()

@register.simple_tag
def patientdays(patient):
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days
    print(patient_admit_date)
    return str(days1)

@register.simple_tag
def depositamount(patient, ind_exp):
    try:
        deposit_date = dateutil.parser.parse(ind_exp.strftime('%m/%d/%Y')).date()
        deposit_amount = PATIENT_DEPOSIT.objects.get(PATIENT_ID=patient, DEPOSIT_DATE=deposit_date).DEPOSIT_AMOUNT
    except:
        deposit_amount = 0
    return str(deposit_amount)

@register.simple_tag
def hosp_debit(ind_exp, patient):
    expense = PATIENT_DAILY_EXPENSE.objects.get(id=ind_exp.id)
    room = patient.PATIENT_ROOM_TYPE
    room_cost = patient.PATIENT_ROOM_PRICE
    # try:
    #     deposit_date = dateutil.parser.parse(ind_exp.strftime('%m/%d/%Y')).date()
    #     deposit_amount = PATIENT_DEPOSIT.objects.get(PATIENT_ID=patient, DEPOSIT_DATE=deposit_date).DEPOSIT_AMOUNT
    # except:
    #     deposit_amount = 0
    deposit_date = dateutil.parser.parse(ind_exp.EXPENSE_DATETIME.strftime('%m/%d/%Y')).date()
    deposit_amount = PATIENT_DEPOSIT.objects.get(PATIENT_ID=patient, DEPOSIT_DATE=deposit_date).DEPOSIT_AMOUNT
    return str(deposit_amount - (expense.RADIOLOGY_EXPENSE+expense.PATHOLOGY_EXPENSE+expense.PHARMACY_EXPENSE+expense.HOSPITAL_EXPANSES+expense.OTHER_EXPENSE) - room_cost - patient.PATIENT_PHYSICIAN_CHARGE)

@register.simple_tag
def physician_visit(patient):
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days
    print(patient_admit_date)
    return str(days1+1)

@register.simple_tag
def deposit_total(patient):
    deposits = PATIENT_DEPOSIT.objects.filter(PATIENT_ID=patient)
    depo_total = 0
    for depo in deposits:
        depo_total += depo.DEPOSIT_AMOUNT
    return str(depo_total)

@register.simple_tag
def radio_total(patient):
    expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
    radio_total = 0
    for radio in expenses:
        radio_total += radio.RADIOLOGY_EXPENSE
    return str(radio_total)

@register.simple_tag
def patho_total(patient):
    expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
    patho_total = 0
    for patho in expenses:
        patho_total += patho.PATHOLOGY_EXPENSE
    return str(patho_total)

@register.simple_tag
def pharma_total(patient):
    expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
    pharma_total = 0
    for pharma in expenses:
        pharma_total += pharma.PHARMACY_EXPENSE
    return str(pharma_total)

@register.simple_tag
def hosp_total(patient):
    expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
    hosp_total = 0
    for hosp in expenses:
        hosp_total += hosp.HOSPITAL_EXPANSES
    return str(hosp_total)

@register.simple_tag
def other_total(patient):
    expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
    other_total = 0
    for other in expenses:
        other_total += other.OTHER_EXPENSE
    return str(other_total)

@register.simple_tag
def grand_total(patient):
    expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
    room = patient.PATIENT_ROOM_TYPE
    room_cost = patient.PATIENT_ROOM_PRICE
    grand_total = 0
    for grand in expenses:
        grand_total += (grand.PATHOLOGY_EXPENSE + grand.PHARMACY_EXPENSE + grand.RADIOLOGY_EXPENSE + grand.HOSPITAL_EXPANSES + grand.OTHER_EXPENSE)
    
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days
    grand_total += room_cost*days1
    grand_total += patient.PATIENT_PHYSICIAN_CHARGE*days1
    deposits = PATIENT_DEPOSIT.objects.filter(PATIENT_ID=patient)
    depo_total = 0
    for depo in deposits:
        depo_total += depo.DEPOSIT_AMOUNT

    hosp_debit_total = depo_total - grand_total
    return str(hosp_debit_total)

@register.simple_tag
def room_type(patient):
    room = patient.PATIENT_ROOM_TYPE
    room_cost = patient.PATIENT_ROOM_PRICE
    return str(room_cost)

@register.simple_tag
def total_room_cost(patient):
    room = patient.PATIENT_ROOM_TYPE
    room_cost = patient.PATIENT_ROOM_PRICE
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days 
    return str(room_cost*days1)

@register.simple_tag
def phy_cost(patient):
    phy_cost = patient.PATIENT_PHYSICIAN_CHARGE
    return str(phy_cost)

@register.simple_tag
def phy_cost_total(patient):
    phy_cost = patient.PATIENT_PHYSICIAN_CHARGE
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days
    return str(phy_cost*days1)