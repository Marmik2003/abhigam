from django import template
from datetime import datetime, timedelta
import dateutil.parser
from ..models import ADMIT_PATIENT, PATIENT_DAILY_EXPENSE, PATIENT_DEPOSIT, ROOM_TYPE, PATIENT_BILL

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
    return str(days1+1)

@register.simple_tag
def depositamount(patient, day):
    patient_admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = patient_admit_date + timedelta(days=int(day))
    try:
        deposit_date = dateutil.parser.parse(this_date.strftime('%m/%d/%Y')).date()
        deposit_amount_all = PATIENT_DEPOSIT.objects.filter(PATIENT_ID=patient, DEPOSIT_DATE=deposit_date)
        deposit_amount = 0
        for depo in deposit_amount_all:
            deposit_amount += depo.DEPOSIT_AMOUNT
    except:
        deposit_amount = 0
    return str(deposit_amount)

@register.simple_tag
def get_date(patient, day):
    admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = admit_date + timedelta(days=int(day))
    return dateutil.parser.parse(this_date.strftime('%d/%m/%Y'))

@register.simple_tag
def radio_pt(patient, day):
    patient_admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = patient_admit_date + timedelta(days=int(day))
    radio_cost = 0
    try:
        expenses = PATIENT_DAILY_EXPENSE.objects.filter(EXPENSE_DATETIME__date=this_date, PATIENT_ID=patient)
        
        for expense in expenses:
            radio_cost += expense.RADIOLOGY_EXPENSE
    except:
        pass
    return str(radio_cost)

@register.simple_tag
def patho_pt(patient, day):
    patient_admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = patient_admit_date + timedelta(days=int(day))
    patho_cost = 0
    try:
        expenses = PATIENT_DAILY_EXPENSE.objects.filter(EXPENSE_DATETIME__date=this_date, PATIENT_ID=patient)
        
        for expense in expenses:
            patho_cost += expense.PATHOLOGY_EXPENSE
    except:
        pass
    return str(patho_cost)

@register.simple_tag
def pharma_pt(patient, day):
    patient_admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = patient_admit_date + timedelta(days=int(day))
    pharma_cost = 0
    try:
        expenses = PATIENT_DAILY_EXPENSE.objects.filter(EXPENSE_DATETIME__date=this_date, PATIENT_ID=patient)
        
        for expense in expenses:
            pharma_cost += expense.PHARMACY_EXPENSE
    except:
        pass
    return str(pharma_cost)

@register.simple_tag
def hosp_pt(patient, day):
    patient_admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = patient_admit_date + timedelta(days=int(day))
    hosp_cost = 0
    try:
        expenses = PATIENT_DAILY_EXPENSE.objects.filter(EXPENSE_DATETIME__date=this_date, PATIENT_ID=patient)
        
        for expense in expenses:
            hosp_cost += expense.HOSPITAL_EXPANSES
    except:
        pass
    return str(hosp_cost)

@register.simple_tag
def other_pt(patient, day):
    patient_admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = patient_admit_date + timedelta(days=int(day))
    other_cost = 0
    try:
        expenses = PATIENT_DAILY_EXPENSE.objects.filter(EXPENSE_DATETIME__date=this_date, PATIENT_ID=patient)
        
        for expense in expenses:
            other_cost += expense.OTHER_EXPENSE
    except:
        pass
    return str(other_cost)

@register.simple_tag
def hosp_debit(patient, day):
    patient_admit_date = patient.PATIENT_ADMIT_DATE_TIME.date()
    this_date = patient_admit_date + timedelta(days=int(day))
    this_date_credit = patient_admit_date + timedelta(days=int(day+1))
    expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient, EXPENSE_DATETIME__lte=this_date_credit)
    room_cost = patient.PATIENT_ROOM_PRICE*day
    # try:
    #     deposit_date = dateutil.parser.parse(ind_exp.strftime('%m/%d/%Y')).date()
    #     deposit_amount = PATIENT_DEPOSIT.objects.get(PATIENT_ID=patient, DEPOSIT_DATE=deposit_date).DEPOSIT_AMOUNT
    # except:
    #     deposit_amount = 0
    
    try:
        deposit_date = dateutil.parser.parse(this_date.strftime('%m/%d/%Y')).date()
        deposit_amount_all = PATIENT_DEPOSIT.objects.filter(PATIENT_ID=patient, DEPOSIT_DATE__lte=deposit_date)
        deposit_amount = 0
        for depo in deposit_amount_all:
            deposit_amount += depo.DEPOSIT_AMOUNT
    except:
        deposit_amount = 0
    total_exp = 0
    try:
        for expense in expenses:
            total_exp += expense.RADIOLOGY_EXPENSE
            total_exp += expense.PATHOLOGY_EXPENSE
            total_exp += expense.PHARMACY_EXPENSE
            total_exp += expense.HOSPITAL_EXPANSES
            total_exp += expense.OTHER_EXPENSE
    except:
        pass
    return str(deposit_amount - total_exp - room_cost - (patient.PATIENT_PHYSICIAN_CHARGE*(day+2)))

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
    return str(days1+1)

@register.simple_tag
def total_individual(patient):
    phy_cost = patient.PATIENT_PHYSICIAN_CHARGE
    room_cost = patient.PATIENT_ROOM_PRICE
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days + 1
    return str((phy_cost+room_cost)*days1 + phy_cost)

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
    days1 = (last_date - patient_admit_date).days + 1
    grand_total += room_cost*days1
    grand_total += patient.PATIENT_PHYSICIAN_CHARGE*(days1)
    deposits = PATIENT_DEPOSIT.objects.filter(PATIENT_ID=patient)
    depo_total = 0
    for depo in deposits:
        depo_total += depo.DEPOSIT_AMOUNT

    hosp_debit_total = depo_total - grand_total
    return str(hosp_debit_total)

@register.simple_tag
def room_type(patient):
    room_cost = patient.PATIENT_ROOM_PRICE
    return str(room_cost)

@register.simple_tag
def total_room_cost(patient):
    room_cost = patient.PATIENT_ROOM_PRICE
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days + 1
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
    days1 = (last_date - patient_admit_date).days + 1
    return str(phy_cost*days1)

@register.simple_tag
def get_discount(patient):
    patient_bill = PATIENT_BILL.objects.get(PATIENT_ID=patient)
    discount = patient_bill.PATIENT_DISCOUNT
    return str(discount)

@register.simple_tag
def total_bill(patient):
    phy_cost = patient.PATIENT_PHYSICIAN_CHARGE
    room_cost = patient.PATIENT_ROOM_PRICE
    patient_admit_datetime = patient.PATIENT_ADMIT_DATE_TIME
    patient_bill = PATIENT_BILL.objects.get(PATIENT_ID=patient)
    try:
        discount = patient_bill.PATIENT_DISCOUNT
    except:
        discount = 0
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        # last_datetime = patient.PATIENT_DISCHARGE_DATE_TIME
        # last_date = dateutil.parser.parse(last_datetime.strftime('%d/%m/%Y')).date()
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = dateutil.parser.parse(patient_admit_datetime.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days + 1
    return str((phy_cost+room_cost)*days1 + phy_cost -discount)