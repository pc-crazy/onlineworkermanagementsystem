# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.
from info.models import User


class WorkerProfile(models.Model):
    user = models.OneToOneField(User, related_query_name=User.objects.filter(type='WO'),blank=True,
                                null=True,related_name='rel_worker_profile')
    city = models.CharField(max_length=155)
    district = models.CharField(max_length=155)
    state = models.CharField(max_length=155)
    address = models.CharField(max_length=155)
    picture =  models.ImageField(upload_to='media',verbose_name='image')
    about = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.get_full_name()


class WorkerSkill(models.Model):
    HIRE_STATUS =  ( ('H', 'Hire'),
                     ('N', 'Not hire'),
                     )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='rel_user_skill',blank=True, null=True)
    experience = models.IntegerField(validators=[MaxValueValidator(100),
                                                 MinValueValidator(0)],default=0)
    skill = models.CharField(max_length=155)
    rate_per_day = models.IntegerField()
    status = models.CharField(choices=HIRE_STATUS, default='N', max_length=1)
    # hired_by = models.ForeignKey(User, related_name='rel_contr_hire',blank=True, null=True)
    # from_date = models.DateField()
    # to_date = models.DateField()

    def __str__(self):
        return self.skill

    class Meta:
        unique_together  = ('user', 'skill')

class HireWorker(models.Model):
    STATUS_CHOICE = (('request','request' ),
                     ('confirm', 'confirm'),
                     ('finish', 'finish'))
    skill = models.ForeignKey(WorkerSkill, related_name='user_worker_skill')
    hired_by = models.ForeignKey(User, related_name='hired_by')
    from_date = models.DateField()
    to_date = models.DateField()
    status = models.CharField(choices = STATUS_CHOICE , max_length=15, default='request')

    def __str__(self):
        return self.skill

class ContractorProfile(models.Model):
    user = models.OneToOneField(User, related_query_name=User.objects.filter(type='CO'),
                                related_name='rel_contractor_profile',blank=True,null=True)
    city = models.CharField(max_length=155)
    district = models.CharField(max_length=155)
    state = models.CharField(max_length=155)
    address = models.CharField(max_length=155)
    picture = models.ImageField(upload_to='media', verbose_name='image')
    about = models.CharField(max_length=255)
    licence =  models.ImageField(upload_to='media', verbose_name='image')


    def __str__(self):
        return self.user.get_full_name()

