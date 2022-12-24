from django.contrib import admin

# Register your models here.
from payments.models import ParentPayment


@admin.register(ParentPayment)
class ParentPaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'parent', 'amount', 'pay_date')

