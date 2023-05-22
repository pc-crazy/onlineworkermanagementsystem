from __future__ import unicode_literals

from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser

from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone_number, first_name, last_name,email ,type, password,  **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        print(phone_number, first_name, last_name,email ,type, password)
        print("phone_number first_name last_name email type password")

        print(password , "password")
        if not phone_number:
            raise ValueError('The given phone_number must be set')
        phone_number = self.normalize_email(phone_number)
        user = self.model(phone_number=phone_number,first_name=first_name,last_name=last_name,email=email,type=type,**extra_fields)
        user.is_active = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number,first_name, last_name,email,type,password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number,first_name,last_name,email,type ,password ,**extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (('CO' ,'contractor'),
                 ('WO', 'Worker'))
    phone_regex = RegexValidator(regex=r'^\d{10}',
                                 message="Phone number must be entered in the format: '999999999'. Up to 10 digits allowed.")
    phone_number = models.CharField(('phone_number'),validators=[phone_regex], unique=True,max_length=12)
    first_name = models.CharField(('first name'), max_length=30, blank=True)
    last_name = models.CharField(('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(('date joined'), auto_now_add=True)
    is_active = models.BooleanField(('active'), default=True)
    is_admin = models.BooleanField(('admin'), default = False)
    is_staff = models.BooleanField(('staff'), default = False)
    type = models.CharField(max_length=2,choices=USER_TYPE ,default='WO')
    email =  models.EmailField(blank=True, null=True, default='')

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def is_contractor(self):
        return self.type == 'CO'

    def is_worker(self):
        print(self.type)
        return  self.type == 'WO'

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name
    #
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     '''
    #     Sends an email to this User.
    #     '''
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    def is_profile_compele(self):
        if self.is_contractor():
            return hasattr(self, 'rel_contractor_profile')
        if  self.is_worker():
            return hasattr(self, 'rel_worker_profile')
