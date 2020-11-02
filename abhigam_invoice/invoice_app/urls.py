from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admit_patient', views.admit_patient, name='admit_patient'),
    path('deposit_amount', views.deposit_amount, name='deposit_amount'),
    path('patient_daily_expenses', views.pt_d_exp, name='pt_d_exp'),
    path('individual_patient_profile', views.ind_pt_prof, name='ind_pt_prof'),
    path('get_patient_prof', views.get_patient_prof, name='get_patient_prof'),
    path('all_patient_profile', views.all_pt_prof, name='all_pt_prof'),
    path('bill_generator', views.bill_generator, name='bill_generator'),
    path('reference_report', views.reference_report, name='reference_report'),
    path('reference_table', views.reference_table, name='reference_table'),
    path('invoice_maker', views.invoice_maker, name='invoice_maker'),
    path('invoice_data', views.invoice_data, name='invoice_data')
]