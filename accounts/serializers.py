from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.core.exceptions import ValidationError as DjangoValidationError
from django.urls import exceptions as url_exceptions
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions, serializers

try:
    from allauth.account import app_settings as allauth_settings
    from allauth.account.adapter import get_adapter
    from allauth.account.utils import setup_user_email
except ImportError:
    raise ImportError('allauth needs to be added to INSTALLED_APPS.')

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer, PasswordResetSerializer
from django.db import transaction

from .forms import CustomPasswordResetForm

User = get_user_model()


class CustomLoginSerializer(LoginSerializer):

    def get_auth_user(self, username, email, password):
        try:
            return self.get_auth_user_using_allauth(username, email, password)
        except url_exceptions.NoReverseMatch:
            msg = _('The email or password you provided is incorrect.')
            raise exceptions.ValidationError(msg)


    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _(
                'This account is currently disabled. Please contact us for more info.')
            raise exceptions.ValidationError(msg)

    @staticmethod
    def validate_email_verification_status(user):
        email_address = user.emailaddress_set.get(email=user.email)
        if not email_address.verified:
            resend_link = "<a href=\"http://127.0.0.1:3000/resend-email-confirmation\">click here.</a>"
            err_msg = (
                f'This email address is not verified. To verify your email {resend_link}')
            raise serializers.ValidationError(_(err_msg))

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(username, email, password)

        if not user:
            msg = _('The email or password you provided is incorrect.')
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs


class CustomRegisterSerializer(RegisterSerializer):
    name = serializers.CharField(
        required=True, allow_blank=False, max_length=100)
    email = serializers.EmailField(required=allauth_settings.EMAIL_REQUIRED)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(required=False)

    def validate_fullname(self, fullname):
        fullname = fullname.split()
        if len(fullname) <= 1:
            raise serializers.ValidationError(
                _('Kindly enter more than one name.'),)
        for x in fullname:
            if len(x) < 2:
                raise serializers.ValidationError(
                    _('Kindly give us your full name.'),)
        return fullname

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }

    def validate(self, data):
        fullname = data['name'].split()
        if len(fullname) <= 1:
            raise serializers.ValidationError(
                _('Kindly enter more than one name.'),)
        for x in fullname:
            if len(x) < 2:
                raise serializers.ValidationError(
                    _('Kindly give us your full name.'),)
        return data

    @transaction.atomic
    def save(self, request):
        # user = super().save(*args, **kwargs)
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user = adapter.save_user(request, user, self, commit=False)
        try:
            adapter.clean_password(self.cleaned_data['password1'], user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(
                detail=serializers.as_serializer_error(exc)
            )
        user.name = self.cleaned_data["name"].title()
        user.save()
        setup_user_email(request, user, [])
        return user


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'name',
        )
        read_only_fields = ('email',)


class CustomPasswordSetSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)

    set_password_form_class = SetPasswordForm
    set_password_form = None

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
        if self.request.user.has_usable_password():
            # return HttpResponseRedirect(reverse("account_change_password"))
            change_password_link = "<a href=\"http://127.0.0.1:3000/change-password\">click here</a>"
            err_msg = (
                f'You\'ve already set a password for this account. To change your password {change_password_link}')
            raise serializers.ValidationError(_(err_msg))

    def validate_old_password(self, value):
        pass

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        return attrs

    def save(self):
        self.set_password_form.save()
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(self.request, self.user)


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'name',
        )
        read_only_fields = ('email',)


class CustomEmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    
class CustomPasswordResetSerializer(PasswordResetSerializer):
    """
    This inherits from dj_rest_auth to solely for custom email
    for password reset
    """
    @property
    def password_reset_form_class(self):
        return CustomPasswordResetForm
