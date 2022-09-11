from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4
from decimal import Decimal


# Create your models here.
class TransactionCategory(models.Model):
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    # Related Field
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="categories", null=True)

    def __str__(self):
        return self.name

    def get_total_cost(self):
        return round(sum(item.amount for item in self.items.all()), 2)
    #     return round(sum(item.amount for item in self.items.filter(
    #         trans_date__year=CurrentYear.objects.all().filter()[:1].get().year)
    #                      ), 2)


class Transaction(models.Model):
    # Related fields
    category = models.ForeignKey(TransactionCategory, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 related_name="items")
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="transactions", null=True)

    #
    Transaction_name = models.CharField(max_length=200, null=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_choices = (
        ('Income', 'Income'),
        ('Expense', 'Expense')
    )
    trans_date = models.DateField(null=True, blank=True)
    Transaction_type = models.CharField(max_length=8, choices=type_choices, blank=True)
    desc = models.CharField(max_length=250, null=True, blank=True)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {}'.format(self.Transaction_name, self.uniqueId))

        self.slug = slugify('{} {}'.format(self.Transaction_name, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Transaction, self).save(*args, **kwargs)
