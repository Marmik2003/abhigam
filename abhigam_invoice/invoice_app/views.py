import os
from django.shortcuts import render, redirect
from pytz import UTC as utc_pytz
from datetime import datetime
from dateutil import parser
from io import BytesIO
from  django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from datetime import datetime, date
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

from .models import *

from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string

def link_callback(uri, rel):
    print("running")
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    result = finders.find(uri)
    if result:
            if not isinstance(result, (list, tuple)):
                    result = [result]
            result = list(os.path.realpath(path) for path in result)
            path=result[0]
    else:
            sUrl = settings.STATIC_URL        # Typically /static/
            sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
            mUrl = settings.MEDIA_URL         # Typically /media/
            mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

            if uri.startswith(mUrl):
                    path = os.path.join(mRoot, uri.replace(mRoot, ""))
            elif uri.startswith(sUrl):
                    path = os.path.join(sRoot, uri.replace(sRoot, ""))
            else:
                    return uri

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                    'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path

def index(request):
    return render(request, 'index.html')

def render_to_pdf(template_src,bill_id , context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="'+ bill_id +'.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=link_callback)
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def admit_patient(request):
    patients = list(ADMIT_PATIENT.objects.all())
    if len(patients) != 0:
        last_patient_id_raw = ADMIT_PATIENT.objects.get(PATIENT_ID = patients[(len(patients)-1)]).PATIENT_ID
        last_patient_id = int(last_patient_id_raw[2:])
    else:
        last_patient_id = 0
    patient_id = "AC" + str(last_patient_id+1)

    if request.method != 'POST':
        doctor_list = PATIENT_TREATING_DR.objects.all()
        room_types = ROOM_TYPE.objects.all()
        return render(request, 'admit_patient.html', context={'patient_id':patient_id, 'doctor_list':doctor_list,'room_types':room_types})

    else:
        patient_name = request.POST['patientName']
        age = request.POST['agebox']
        fatherName = request.POST['fatherName']
        gender = request.POST['gender']
        birthDate = request.POST['birthDate']
        admitDate = request.POST['admitDate']
        admitTime = request.POST['admitTime']
        referby = request.POST['referby']
        information_givenby = request.POST['information_givenby']
        patient_email = request.POST['patient_email']
        emailrelative = request.POST['emailrelative']
        patientPhone = request.POST['patientPhone']
        Phonerelative = request.POST['Phonerelative']
        relation = request.POST['relation']
        idproofname = request.POST['idproofname']
        idproofnumber = request.POST['idproofnumber']
        inputAddress1 = request.POST['inputAddress1']
        inputAddress2 = request.POST['inputAddress2']
        inputCity = request.POST['inputCity']
        inputDistrict = request.POST['inputDistrict']
        inputState = request.POST['inputState']
        inputPin = request.POST['inputPin']
        treating_doctor_raw = request.POST['treating_doctor']
        physician_charge = request.POST['physician_charge']
        mediclaim = request.POST['mediclaim']
        room_category_raw = request.POST['roomCategory']
        room_price = request.POST['room_price']
        admitDateTime = admitDate + " " + admitTime

        teating_doctor = PATIENT_TREATING_DR.objects.get(id = treating_doctor_raw)
        room_category  = ROOM_TYPE.objects.get(id=room_category_raw)

        patient_save = ADMIT_PATIENT(
            PATIENT_ID=patient_id, 
            PATIENT_NAME=patient_name, 
            PATIENT_AGE=age, 
            PATIENT_FHR_HUS_NAME=fatherName, 
            PATIENT_ADMIT_DATE_TIME=admitDateTime,
            PATIENT_BIRTH_DATE=birthDate,
            PATIENT_SEX=gender,
            PATIENT_REFER_BY=referby,
            PATIENT_INFORMATION_GIVEN_BY=information_givenby,
            PATIENT_EMAIL_ID=patient_email,
            PATIENT_RELATIVE_EMAIL=emailrelative,
            PATIENT_MOB_NUM=patientPhone,
            PATIENT_RELATIVE_MOB_NUM=Phonerelative,
            PATIENT_RELATION=relation,
            PATIENT_ID_PROOF_NAME=idproofname,
            PATIENT_ID_PROOF_NUMBER=idproofnumber,
            PATIENT_STREET1 = inputAddress1,
            PATIENT_STREET2=inputAddress2,
            PATIENT_CITY=inputCity,
            PATIENT_DISTRICT=inputDistrict,
            PATIENT_STATE=inputState,
            PATIENT_PINCODE=inputPin,
            PATIENT_TREATING_DR=teating_doctor,
            PATIENT_PHYSICIAN_CHARGE=physician_charge,
            PATIENT_MED_CLAIM=mediclaim,
            PATIENT_ROOM_TYPE=room_category,
            PATIENT_ROOM_PRICE=room_price
        )
        patient_save.save()
        patient_pdf_data = ADMIT_PATIENT.objects.get(PATIENT_ID=patient_id)
        pdf = render_to_pdf('pdf_admit_patient.html',('PatientId'+patient_id),{'patient':patient_pdf_data})
        return HttpResponse(pdf, content_type='application/pdf')

def deposit_amount(request):
    if request.method != 'POST':
        patients = ADMIT_PATIENT.objects.all()
        return render(request, 'deposit_amount.html', context={'patients':patients})
    else:
        patient_id = request.POST['patient_id']
        deposit_amount = request.POST['deposit_amount']
        deposit_date = request.POST['deposit_date']
        try:
            patient = ADMIT_PATIENT.objects.get(PATIENT_ID=patient_id)
        except:
            messages.error(request, 'Patient not found')
            return redirect('deposit_amount')
        deposit = PATIENT_DEPOSIT(PATIENT_ID=patient,DEPOSIT_AMOUNT=deposit_amount,DEPOSIT_DATE=deposit_date)
        deposit.save()
        messages.success(request, 'Amount deposited to the Patient ' + patient.PATIENT_NAME + ' Successfully!')
        return redirect('deposit_amount')

def patientsearch(request):
    patient_id = request.GET.get('patient_id')
    patient_name = ADMIT_PATIENT.objects.get(PATIENT_ID=patient_id).PATIENT_NAME
    father_name = ADMIT_PATIENT.objects.get(PATIENT_ID=patient_id).PATIENT_FHR_HUS_NAME
    return render(request, 'partials/patient_search.html', context={'patient_name':patient_name,'father_name':father_name})

def pt_d_exp(request):
    if request.method != 'POST':
        patients = ADMIT_PATIENT.objects.all()
        return render(request, 'pt_d_exp.html', context={'patients':patients})
    else:
        patient_id = request.POST['patient_id']
        expenseDateTime = request.POST['expenseDate'] + " " + request.POST['expenseTime']
        radioCost = request.POST['Radiology']
        pathoCost = request.POST['Pathology']

        #here is change
        pharmaCost = request.POST['Pharmacy']
        hospCost = request.POST['Hospital_Expenses']
        otherCost = request.POST['Other']
        try:
            remarks = request.POST['remarks']
        except:
            remarks = "No remarks"
        
        try:
            patient = ADMIT_PATIENT.objects.get(PATIENT_ID=patient_id)
        except:
            messages.error(request, 'Patient id '+ patient_id +' not found')
            return redirect('pt_d_exp')

        pt_d_exp_save = PATIENT_DAILY_EXPENSE(PATIENT_ID=patient, EXPENSE_DATETIME=expenseDateTime, RADIOLOGY_EXPENSE=radioCost,PATHOLOGY_EXPENSE=pathoCost,PHARMACY_EXPENSE=pharmaCost,HOSPITAL_EXPANSES=hospCost,OTHER_EXPENSE=otherCost,REMARKS=remarks)
        pt_d_exp_save.save()
        messages.success(request,'Daily Expense of '+ patient.PATIENT_NAME +' added for date '+ request.POST['expenseDate'])
        return redirect('pt_d_exp')

def ind_pt_prof(request):
    patients = ADMIT_PATIENT.objects.all()
    
    return render(request, 'ind_pt_prof.html', context={'patients':patients})

def get_patient_prof(request):
    patient_id = request.GET.get('patient_id')
    patient = ADMIT_PATIENT.objects.get(PATIENT_ID=patient_id)
    if patient.PATIENT_DISCHARGE_DATE_TIME != None:
        last_date = patient.PATIENT_DISCHARGE_DATE_TIME.date()
    else:
        last_date = datetime.now().date()
    patient_admit_date = parser.parse(patient.PATIENT_ADMIT_DATE_TIME.strftime('%m/%d/%Y')).date()
    days1 = (last_date - patient_admit_date).days + 1
    pt_d_exp_all = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
    return render(request, 'partials/ind_expense_table.html', context={'pt_d_exp_all':pt_d_exp_all, 'patient':patient, 'days':list(range(days1+1))})

def all_pt_prof(request):
    patients = ADMIT_PATIENT.objects.all()
    deposit_dict = {}
    days_dict = {}
    physician_visit_dict = {}
    radiology_dict = {}
    pathology_dict = {}
    pharmacy_dict = {}
    hospital_expense_dict = {}
    other_expense_dict = {}
    for patient in patients:
        deposit_pt = PATIENT_DEPOSIT.objects.filter(PATIENT_ID=patient)
        depopt = 0
        for depo in deposit_pt:
            depopt1 = depo.DEPOSIT_AMOUNT
            depopt += depopt1
        now = datetime.now().astimezone(utc_pytz)
        now_utc = now.replace(tzinfo=utc_pytz)
        if patient.PATIENT_DISCHARGE_DATE_TIME == None:
            days = (now_utc-patient.PATIENT_ADMIT_DATE_TIME).days
        else:
            days = (patient.PATIENT_DISCHARGE_DATE_TIME-patient.PATIENT_ADMIT_DATE_TIME).days
        days_dict[patient] = days
        deposit_dict[patient] = str(depopt)
        physician_visit = days+1
        physician_visit_dict[patient] = physician_visit
        expenses = PATIENT_DAILY_EXPENSE.objects.filter(PATIENT_ID=patient)
        rexp = 0
        pexp = 0
        phexp = 0
        hexp = 0
        oexp = 0
        for expense in expenses:
            rexp += int(expense.RADIOLOGY_EXPENSE)
            pexp += int(expense.PATHOLOGY_EXPENSE)
            phexp += int(expense.PHARMACY_EXPENSE)
            hexp += int(expense.HOSPITAL_EXPANSES)
            oexp += int(expense.OTHER_EXPENSE)
        radiology_dict[patient] = str(rexp)
        pathology_dict[patient] = str(pexp)
        pharmacy_dict[patient] = str(phexp)
        hospital_expense_dict[patient] = str(hexp)
        other_expense_dict[patient] = str(oexp)

    return render(request, 'all_pt_prof.html', context={'patients':patients, 'deposit_dict':deposit_dict})

def bill_generator(request):
    bills = list(PATIENT_BILL.objects.all())
    if len(bills) != 0:
        last_bill_id_raw = PATIENT_BILL.objects.get(PATIENT_BILL_NO = bills[(len(bills)-1)]).PATIENT_BILL_NO
        print(last_bill_id_raw)
        last_bill_id = int(last_bill_id_raw[3:])
    else:
        last_bill_id = 0
    bill_id = "ACB" + str(last_bill_id+1)
    print(bill_id)
    if request.method != 'POST':
        return render(request, 'bill_generator.html', context={'billno':bill_id})
    else:
        patient_id = request.POST['patient_id']
        now = datetime.now().astimezone(utc_pytz)
        now_utc = now.replace(tzinfo=utc_pytz)
        pan_no = "ABSFA9076B"
        cin_no = "137C0004672"
        patient = ADMIT_PATIENT.objects.get(PATIENT_ID=patient_id)
        patient.PATIENT_DISCHARGE_DATE_TIME = now_utc
        patient.save()
        bill_data = PATIENT_BILL(PATIENT_ID=patient, PAN_NO=pan_no, CIN_NO=cin_no,PATIENT_BILL_NO=bill_id)
        bill_data.save()
        data = {'patient':patient,'cin_no':cin_no,'pan_no':pan_no,'bill_id':bill_id}
        pdf = render_to_pdf('pdf_template.html', bill_id, data)
        return HttpResponse(pdf, content_type='application/pdf')

def reference_report(request):
    patients = ADMIT_PATIENT.objects.all()
    doctors = []
    for patient in patients:
        if patient.PATIENT_REFER_BY in doctors:
            pass
        else:
            doctors.append(patient.PATIENT_REFER_BY)
    return render(request,'reference_report.html', context={'doctors':doctors})

def reference_table(request):
    dr = request.GET.get('Dr')
    patients = ADMIT_PATIENT.objects.filter(PATIENT_REFER_BY=dr)
    return render(request, 'reference_table.html', context={'patients':patients})

def patient_status(request):
    return render(request, 'patient_status.html')

def patient_status_table(request):
    status = request.GET.get('patient_status')
    if status == 'active':
        patients = ADMIT_PATIENT.objects.filter(PATIENT_DISCHARGE_DATE_TIME=None)
        return render(request, 'partials/active_patient_table.html', context={'patients':patients})
    else:
        patients = ADMIT_PATIENT.objects.exclude(PATIENT_DISCHARGE_DATE_TIME=None)
        return render(request, 'partials/inactive_patient_table.html', context={'patients':patients})

def invoice_maker(request):
    if request.method != 'POST':
        return render(request, 'invoice_maker.html')
    else:
        patient_name    = request.POST['patient_name']
        admit_date      = request.POST['admit_date']
        discharge_date  = request.POST['discharge_date']
        days            = request.POST['days']
        cpd             = request.POST['cpd']
        phy_visit       = request.POST['phy_visit']
        total_bill      = request.POST['total_bill']
        deposit         = request.POST['deposit']
        discount        = request.POST['discount']
        hosp_credit     = request.POST['hosp_credit']
        data = {'patient_name':patient_name, 'admit_date':admit_date, 'discharge_date':discharge_date, 'days':days, 'cpd':cpd, 'phy_visit':phy_visit, 'total_bill': total_bill, 'deposit':deposit, 'discount':discount, 'hosp_credit':hosp_credit}

        pdf = render_to_pdf('pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

def invoice_data(request):
    return render(request,'invoice_data.html')

def fixed_charges(request):
    return render(request, 'fixed_charges.html')
