from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.core.validators import RegexValidator
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        account = self.model(
            email=self.normalize_email(email),
            full_name=kwargs.get('full_name'),
        )

        account.special_key = User.objects.make_random_password(length=6, allowed_chars='0123456789')

        account.set_password(password)

        account.save()

        return account


class StoreManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):

        # print("ok")

        if not email:
            raise ValueError('Users must have a valid email address.')

        if not kwargs.get('country'):
            raise ValueError('Users must select a country.')

        if not kwargs.get('gender'):
            raise ValueError('Users must select a gender.')

        if not kwargs.get('phone'):
            raise ValueError('Users must have a valid phone number.')

        if not kwargs.get('size'):
            raise ValueError('Users must select a shoe size.')

        temp = Account.objects.get(email=email)

        account = self.model(
            email=self.normalize_email(temp.email),
            full_name=temp.full_name,
            special_key=temp.special_key,
            phone_number=kwargs.get('phone'),
            is_valid=False,
            shoe_size=kwargs.get('size'),
            country=kwargs.get('country'),
            gender=kwargs.get('gender'),
            password=temp.password,
        )

        account.set_password(password)

        account.save()

        return account


class DeliveryManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):

        if not kwargs.get('country'):
            raise ValueError('Users must select a country.')

        if not kwargs.get('gender'):
            raise ValueError('Users must select a gender.')

        if not kwargs.get('phone_number'):
            raise ValueError('Users must have a valid phone number.')

        if not kwargs.get('shoe_size'):
            raise ValueError('Users must select a shoe size.')

        temp = Account.objects.get(email=email)

        account = self.model(
            email=self.normalize_email(temp.email),
            full_name=temp.full_name,
            special_key=temp.special_key,
            phone_number=kwargs.get('phone'),
            is_valid=False,
            shoe_size=kwargs.get('size'),
            country=kwargs.get('country'),
            gender=kwargs.get('gender'),
            password=temp.password,
        )

        account.set_password(password)

        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False, )

    full_name = models.CharField(max_length=40, blank=False, default="Fake Name")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15, unique=True, null=True)  # validators should be a list

    special_key = models.CharField(max_length=6, blank=True, default="123456")

    #will be used for sms verification
    is_valid = models.BooleanField(default=False)

    #used for email verification
    is_active = models.BooleanField(default=False)

    shoe_size = models.IntegerField(blank=True, null=True)
    buying_option = models.CharField(max_length=40, blank=True, default="Store")
    has_submitted_shoe = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __unicode__(self):
        return self.email



class StoreAccount(AbstractBaseUser):
    email = models.EmailField(unique=False, blank=False)

    full_name = models.CharField(max_length=40, blank=False, default="Fake Name")

    phone_number = models.CharField(blank=True, max_length=15, unique=True, null=True)  # validators should be a list

    special_key = models.CharField(max_length=6, blank=True, default="123456")

    #will be used for sms verification
    is_valid = models.BooleanField(default=False)

    shoe_size = models.CharField(max_length=3, blank=True, null=True)

    country = models.CharField(max_length=40, blank=False, default="Not a real country")

    birth_date = models.CharField(max_length=15, blank=False, default="01/01/1111")
    gender = models.CharField(max_length=3, blank=False, default="N/A")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = StoreManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number', 'special_key', 'is_valid', 'shoe_size', 'country',
                       'birth_date', 'gender']

    def __unicode__(self):
        return self.email


class OnlineAccount(AbstractBaseUser):
    email = models.EmailField(unique=False, blank=False)

    full_name = models.CharField(max_length=40, blank=False, default="Fake Name")

    phone_number = models.CharField(blank=True, max_length=15, unique=True, null=True)  # validators should be a list

    special_key = models.CharField(max_length=6, blank=True, default="123456")

    #will be used for sms verification
    is_valid = models.BooleanField(default=False)

    shoe_size = models.CharField(max_length=3, blank=True, null=True)

    country = models.CharField(max_length=40, blank=False, default="Not a real country")

    birth_date = models.CharField(max_length=15, blank=False, default="01/01/1111")
    gender = models.CharField(max_length=3, blank=False, default="N/A")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DeliveryManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number', 'special_key', 'is_valid', 'shoe_size', 'country',
                       'birth_date', 'gender']

    def __unicode__(self):
        return self.email

