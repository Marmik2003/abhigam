from django.shortcuts import render
from io import BytesIO
from  django.template.loader import get_template
from django.http import HttpResponse\

from xhtml2pdf import pisa

def index(request):
    return render(request, 'index.html')

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

# Create your views here.
def dashboard(request):
    return render(request, 'dashboard.html')

def admit_patient(request):
    return render(request, 'admit_patient.html')

def deposit_amount(request):
    return render(request, 'deposit_amount.html')

def pt_d_exp(request):
    return render(request, 'pt_d_exp.html')

def ind_pt_prof(request):
    return render(request, 'ind_pt_prof.html')

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
