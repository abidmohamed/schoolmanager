from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.utils import timezone
from uuid import uuid4


# Create your models here.
class Parent(models.Model):
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
    # Related Fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="parents", null=True)
    profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name="parent_profile", null=True)
    # basic
    name = models.CharField(null=True, blank=True, max_length=200)
    address = models.CharField(null=True, blank=True, max_length=200)
    province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    phone = models.CharField(null=True, blank=True, max_length=100)
    email = models.CharField(null=True, blank=True, max_length=100)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)
    date_joined = models.DateField(null=True)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.province, self.uniqueId)

    def get_absolute_url(self):
        return reverse('parent-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.name, self.province, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.name, self.province, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Parent, self).save(*args, **kwargs)


class Kids(models.Model):
    # Related Fields
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="kids", null=True)
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE, related_name="my_kids", null=True)
    # basic Fields
    name = models.CharField(null=True, blank=True, max_length=200)
    grade = models.CharField(null=True, blank=True, max_length=200)
    sick = models.BooleanField(default=False)
    description = models.TextField(max_length=400, null=True)
    birthday = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    transportation = models.BooleanField(default=False)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.grade, self.uniqueId)

    def get_absolute_url(self):
        return reverse('kids-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.name, self.grade, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.name, self.grade, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Kids, self).save(*args, **kwargs)


class Student(models.Model):
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
    # Related Fields
    # Related Field
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="students", null=True)
    # basic
    name = models.CharField(null=True, blank=True, max_length=200)
    address = models.CharField(null=True, blank=True, max_length=200)
    province = models.CharField(choices=PROVINCES, blank=True, max_length=100)
    phone = models.CharField(null=True, blank=True, max_length=100)
    email = models.EmailField(null=True, blank=True, max_length=100)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)
    date_joined = models.DateField(null=True)
    birthday = models.DateField(null=True)
    is_active = models.BooleanField(default=True)
    transportation = models.BooleanField(default=False)

    # Utility fields
    uniqueId = models.CharField(null=True, blank=True, max_length=100)
    slug = models.SlugField(max_length=500, unique=True, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.name, self.province, self.uniqueId)

    def get_absolute_url(self):
        return reverse('parent-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if self.date_created is None:
            self.date_created = timezone.localtime(timezone.now())
        if self.uniqueId is None:
            self.uniqueId = str(uuid4()).split('-')[4]
            self.slug = slugify('{} {} {}'.format(self.name, self.province, self.uniqueId))

        self.slug = slugify('{} {} {}'.format(self.name, self.province, self.uniqueId))
        self.last_updated = timezone.localtime(timezone.now())

        super(Student, self).save(*args, **kwargs)
