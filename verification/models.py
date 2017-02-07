from __future__ import unicode_literals


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.core.validators import RegexValidator
from simple_email_confirmation.models import SimpleEmailConfirmationUserMixin

from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have a valid email address.')

        # if not kwargs.get('phone_number'):
        #     raise ValueError('Users must have a valid phone number.')

        # if not kwargs.get('full_name'):
        #     raise ValueError('Users must have a valid name.')

        account = self.model(
            email=self.normalize_email(email),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name'),
            phone_number=kwargs.get('phone_number'),
        )

        account.special_key = User.objects.make_random_password(length=6, allowed_chars='0123456789')

        account.set_password(password)
        account.save()

        return account


class Account(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False)

    first_name = models.CharField(max_length=40, blank=False, default="Steve")
    last_name = models.CharField(max_length=40, blank=False, default="Jobs")

    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. "
                                         "Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15, unique=True, null=True)  # validators should be a list

    password = models.CharField(max_length=15, blank=False)

    special_key = models.CharField(max_length=15, blank=True, default="123456")

    is_valid = models.BooleanField(default=False)
    has_submitted_shoe = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #delete_at = models.DateTimeField()

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __unicode__(self):
        return self.email