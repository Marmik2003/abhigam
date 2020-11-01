from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('admit_patient', views.admit_patient, name='admit_patient'),
    path('invoice_maker', views.invoice_maker, name='invoice_maker'),
    path('invoice_data', views.invoice_data, name='invoice_data')
]