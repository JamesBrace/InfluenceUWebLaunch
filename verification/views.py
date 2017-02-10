from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core import signing
from django.core.mail import EmailMessage
from django.urls import reverse
from rest_framework import permissions, viewsets, status, views
from rest_framework.response import Response

from vendor.registration import signals
from vendor.registration.views import ActivationView as BaseActivationView
from verification.models import Account, StoreAccount, OnlineAccount
from verification.permissions import IsAccountOwner
from verification.serializers import AccountSerializer, ResponseSerializer, LoginSerializer, UpdateSerializer
import re

from twilio import twiml
from twilio.rest import TwilioRestClient

from django_twilio.decorators import twilio_view


REGISTRATION_SALT = getattr(settings, 'REGISTRATION_SALT', 'registration')


class AccountViewSet(viewsets.ModelViewSet):
    lookup_field = 'email'
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    """
        Register a new (inactive) user account, generate an activation key
        and email it to the user.

        This is different from the model-based activation workflow in that
        the activation key is simply the username, signed using Django's
        TimestampSigner, with HMAC verification on activation.

    """


    # def register(self, form):
    #
    #     return new_user

    def get_success_url(self, user):
        return ('registration_complete', (), {})

    def create_inactive_user(self, **kwargs):
        """
        Create the inactive user account and send an email containing
        activation instructions.

        """
        new_user = Account.objects.create_user(**kwargs)
        new_user.is_active = False
        new_user.save()

        self.send_activation_email(new_user)

        return new_user

    def get_activation_key(self, user):
        """
        Generate the activation key which will be emailed to the user.

        """
        return signing.dumps(
            obj=getattr(user, user.USERNAME_FIELD),
            salt=REGISTRATION_SALT
        )

    def get_email_context(self, activation_key):
        """
        Build the template context used for the activation email.

        """

        return {
            'activation_key': activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': get_current_site(self.request),
        }

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is simply the
        username, signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user
        })

        action_url = "https://releases.influenceu.com" + reverse('registration_activate', kwargs={'activation_key':activation_key})

        message = EmailMessage(
            subject=None,
            body=None,
            to=[user.email],  #
        )
        message.template_id = 1288922  # use this Postmark template

        message.merge_global_data = {
            'name': user.full_name,
            'action_url': action_url
        }

        message.send()

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        if self.request.method == 'POST':
            return permissions.AllowAny(),
        return permissions.IsAuthenticated(), IsAccountOwner()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        data = request.data
        email = data.get('email', None)

        exists = Account.objects.filter(email=email).exists()

        if exists:
            return Response({
                'status': 'error',
                'message': 'Email has already been registered.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid():
            account = self.create_inactive_user(**serializer.validated_data)
            signals.user_registered.send(sender=self.__class__,
                                         user=account,
                                         request=self.request)
            serialized = ResponseSerializer(account)
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class ActivationView(BaseActivationView):
    """
    Given a valid activation key, activate the user's
    account. Otherwise, show an error message stating the account
    couldn't be activated.

    """
    def activate(self, *args, **kwargs):
        # This is safe even if, somehow, there's no activation key,
        # because unsign() will raise BadSignature rather than
        # TypeError on a value of None.
        username = self.validate_key(kwargs.get('activation_key'))

        if username is not None:
            user = self.get_user(username)
            if user is not None:
                user.is_active = True
                print(user.is_active)
                user.save()
                return user
        return False

    def get_success_url(self, user):
        return ('registration_activation_complete', (), {})

    def validate_key(self, activation_key):
        """
        Verify that the activation key is valid and within the
        permitted activation time window, returning the username if
        valid or ``None`` if not.

        """
        try:
            username = signing.loads(
                activation_key,
                salt=REGISTRATION_SALT,
                max_age=settings.ACCOUNT_ACTIVATION_DAYS * 86400
            )
            return username
        # SignatureExpired is a subclass of BadSignature, so this will
        # catch either one.
        except signing.BadSignature:
            return None

    def get_user(self, username):
        """
        Given the verified username, look up and return the
        corresponding user account if it exists, or ``None`` if it
        doesn't.

        """
        try:
            user = Account.objects.get(email=username)
            return user
        except Account.DoesNotExist:
            return None

class ResendView(views.APIView):
    email_body_template = 'registration/activation_email.txt'
    email_subject_template = 'registration/activation_email_subject.txt'

    def post(self, request, format=None):
        data = request.data
        email = data.get('email', None)

        exists = Account.objects.filter(email=email).exists()

        if not exists:
            return Response({
                'status': 'error',
                'message': 'Somehow sent an invalid email...probably some crazy hacka'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = Account.objects.get(email=email)
        self.send_activation_email(user)
        signals.user_registered.send(sender=self.__class__, user=user, request=self.request)
        return Response("Email was resent successfully!", status=status.HTTP_200_OK)


    def get_activation_key(self, user):
        """
        Generate the activation key which will be emailed to the user.

        """
        return signing.dumps(
            obj=getattr(user, user.USERNAME_FIELD),
            salt=REGISTRATION_SALT
        )

    def get_email_context(self, activation_key):
        """
        Build the template context used for the activation email.

        """
        return {
            'activation_key': activation_key,
            'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
            'site': get_current_site(self.request)
        }

    def send_activation_email(self, user):
        """
        Send the activation email. The activation key is simply the
        username, signed using TimestampSigner.

        """
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context.update({
            'user': user
        })

        action_url = "https://releases.influenceu.com" + reverse('registration_activate',
                                                               kwargs={'activation_key': activation_key})

        print(action_url)

        message = EmailMessage(
            subject=None,
            body=None,
            to=[user.email],  #
        )
        message.template_id = 1288922  # use this Postmark template

        message.merge_global_data = {
            'name': user.full_name,
            'action_url': action_url
        }

        message.send()


class LoginView(views.APIView):
    def post(self, request, format=None):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)

        exists = Account.objects.filter(email=email).exists()

        if not exists:
            return Response({
                'status': 'Unauthorized',
                'message': 'We do not have an account under this email.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        temp = Account.objects.get(email=email)

        print(temp.is_valid)

        if not temp.is_active:
            return Response({
                'status': 'Unauthorized',
                'message': 'You have to verify your email before logging in.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        if temp.is_valid:
            return Response({
                'status': 'Unauthorized',
                'message': 'You have already logged in and updated your information.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        account = authenticate(email=email, password=password)

        # fail, bad login info
        if account is None:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination invalid.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # fail, inactive account
        if not account.is_active:
            return Response({
                'status': 'Unauthorized',
                'message': 'This account has not been email verified.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # success, login and respond
        login(request, account)
        serialized = LoginSerializer(account)
        return Response(serialized.data, status=status.HTTP_201_CREATED)


class Temp(object):
    def __init__(self, email_, full_name, phone_number, special_key, shoe_size, country, gender):
        self.email = email_
        self.full_name = full_name
        self.phone_number = phone_number
        self.special_key = special_key
        self.shoe_size = shoe_size
        self.country = country
        self.gender = gender

class UpdateView(views.APIView):
    serializer_class = UpdateSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return permissions.AllowAny(),
        if self.request.method == 'POST':
            return permissions.AllowAny(),
        return permissions.IsAuthenticated(), IsAccountOwner()

    def post(self, request):

        data_ = request.data.copy()
        phone = data_.get('phone')
        new_phone = re.sub("[^0-9]", "", phone)
        # data['phone'] = new_phone

        option = data_.get('option')
        email = data_.get('email')

        account = Account.objects.get(email=email)

        serializer = UpdateSerializer(data={'email':data_.get('email'), 'full_name': account.full_name, 'phone':new_phone,
                                            'special_key':account.special_key, 'size':data_.get('size'),
                                            'country':data_.get('country'),'gender':data_.get('gender'), 'option':option})

        serializer.is_valid()

        print("serialized data: ")
        print(serializer.data)

        in_store = option == "in_store"

        if in_store:
            if serializer.is_valid():

                store_account = StoreAccount.objects.create_user(**serializer.validated_data)


                message_body = "InfluenceU: You're almost there! Your verification code is: " + account.special_key

                account_sid = settings.TWILIO_ACCOUNT_SID
                auth_token = settings.TWILIO_AUTH_TOKEN
                client = TwilioRestClient(account_sid, auth_token)

                send_number = "+" + new_phone

                try:
                    message = client.messages.create(to=send_number, from_="+14387924136", body=message_body)
                except ValueError:
                    store_account.delete()
                    return Response({
                        'status': 'error',
                        'message': 'Could not send the text. Invalid number'
                    }, status=status.HTTP_400_BAD_REQUEST)

                return Response({
                                    'status': 'success',
                                    'message': 'Sent the text successfully'
                                }, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response("Error in updating account", status=status.HTTP_400_BAD_REQUEST)
        else:
            if serializer.is_valid():
                online_account = OnlineAccount.objects.create_user(**serializer.validated_data)
                serialized = ResponseSerializer(online_account)

                # add twilio shit here
                message = "InfluenceU: You're almost there! Your verification code is: " + account.special_key

                print("saving to in store database")

                return Response(serialized.data, status=status.HTTP_201_CREATED)
            else:
                return Response("Error in updating account", status=status.HTTP_400_BAD_REQUEST)


class VerifyView(views.APIView):
    def post(self, request, format=None):
        data = request.data
        special_key = data.get('special_key', None)
        email = data.get('email', None)

        temp = Account.objects.get(email=email)
        temp_special_key = temp.special_key

        if special_key == temp_special_key:
            temp.is_valid = True
            print (temp.is_valid)
            return Response({
                'status': True,
                'message': 'You have been successfully verified!'
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Invalid code, try again.'
            }, status=status.HTTP_401_UNAUTHORIZED)
