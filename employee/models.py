from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4


# Create your models here.
class Role(models.Model):
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="roles", null=True)
    # basic fields
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=200)

    def __str__(self):
        return self.name


class Employee(models.Model):
    PROVINCES = [
        ('Adrar', 'Adrar'),
        ('Chlef', 'Chlef'),
        ('Laghouat', 'Laghouat'),
        ('Oum El Bouaghi', 'Oum El Bouaghi'),
        ('Batna', 'Batna'),
        ('Béjaïa', 'Béjaïa'),
        ('Biskra', 'Biskra'),
        ('Béchar', 'Béchar'),
        ('Blida', 'Blida'),
        ('Bouïra', 'Bouïra'),
        ('Tamanrasset', 'Tamanrasset'),
        ('Tébessa', 'Tébessa'),
        ('Tlemcen', 'Tlemcen'),
        ('Tiaret', 'Tiaret'),
        ('Tizi Ouzou', 'Tizi Ouzou'),
        ('Algiers', 'Algiers'),
        ('Djelfa', 'Djelfa'),
        ('Jijel', 'Jijel'),
        ('Sétif', 'Sétif'),
        ('Saïda', 'Saïda'),
        ('Skikda', 'Skikda'),
        ('Sidi Bel Abbès', 'Sidi Bel Abbès'),
        ('Annaba', 'Annaba'),
        ('Guelma', 'Guelma'),
        ('Constantine', 'Constantine'),
        ('Médéa', 'Médéa'),
        ('Mostaganem', 'Mostaganem'),
        ('M Sila', 'M Sila'),
        ('Mascara', 'Mascara'),
        ('Ouargla', 'Ouargla'),
        ('Oran', 'Oran'),
        ('El Bayadh', 'El Bayadh'),
        ('Illizi', 'Illizi'),
        ('Bordj Bou Arréridj', 'Bordj Bou Arréridj'),
        ('Boumerdes', 'Boumerdes'),
        ('El Taref', 'El Taref'),
        ('Tindouf', 'Tindouf'),
        ('Tissemsilt', 'Tissemsilt'),
        ('El Oued', 'El Oued'),
        ('Khenchela', 'Khenchela'),
        ('Souk Ahras', 'Souk Ahras'),
        ('Tipaza', 'Tipaza'),
        ('Mila', 'Mila'),
        ('Ain Defla', 'Ain Defla'),
        ('Naâma', 'Naâma'),
        ('Ain Timouchent', 'Ain Timouchent'),
        ('Ghardaia', 'Ghardaia'),
        ('Relizane', 'Relizane'),
        ('El M Ghair', 'El M Ghair'),
        ('El Menia', 'El Menia'),
        ('Ouled Djellal', 'Ouled Djellal'),
        ('Bordj Baji Mokhtar', 'Bordj Baji Mokhtar'),
        ('Béni Abbès', 'Béni Abbès'),
        ('Timimoun', 'Timimoun'),
        ('Touggourt', 'Touggourt'),
        ('Djanet', 'Djanet'),
        ('In Salah', 'In Salah'),
        ('In Guezzam', 'In Guezzam'),
    ]
    GENDER = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    MARTIAL = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
    ]
    # related fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="employees", null=True)
    role = models.ForeignKey(Role, on_delete=models.DO_NOTHING, related_name="role_employees", null=True)
    # basic fields
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.CharField(null=True, blank=True, max_length=200)
    province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    gender = models.CharField(choices=GENDER, blank=True, max_length=100)
    martial_status = models.CharField(choices=MARTIAL, blank=True, max_length=100)
    date_joined = models.DateField(null=True)
    birth_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.province)

    def get_absolute_url(self):
        return reverse('employee-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.name, self.province, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.name, self.province, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Employee, self).save(*args, **kwargs)
