from . import views
from django.urls import path

app_name = 'payments'

urlpatterns = [
    path('payments', views.payments, name="payments"),

    # Students Payments
    path('students-payments', views.student_payments, name="students_payments"),
    path('students-payments/details/<slug:slug>', views.student_payment_details, name="student_payment_details"),

    # Parents Payments
    path('parents-payments', views.parent_payments, name="parents_payments"),
    path('parents-payments/details/<slug:slug>', views.parent_payment_details, name="parent_payment_details"),

    # Payrolls
    path('payrolls', views.payrolls, name="payrolls"),
    path('payrolls/details/<slug:slug>', views.payroll_details, name="payroll_details"),
    path('payrolls/pay/<slug:slug>', views.payroll_paid, name="payroll_paid"),

    # API urls
    path('api/parents-payments', views.ParentPaymentView.as_view(), name="api_parents_payments"),

]
