from . import views
from django.urls import path

app_name = 'caisse'

urlpatterns = [
    # cash register
    path('', views.cash_register, name='cash_register'),

    # Category
    path('transaction_category_list/', views.transaction_category_list, name='transaction_category_list'),
    path('transaction_category_details/<str:pk>', views.transaction_category_details,
         name='transaction_category_details'),

    # Transaction
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('transaction_details/<slug:slug>', views.transaction_details, name='transaction_details'),
    path('transaction_update/<slug:slug>', views.transaction_update, name='transaction_update'),
    path('transaction_delete/<slug:slug>', views.transaction_delete, name='transaction_delete'),

]
