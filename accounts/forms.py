from allauth.account.adapter import get_adapter
from allauth.account.forms import EmailAwarePasswordResetTokenGenerator
from allauth.account.models import EmailAddress
from allauth.account.utils import user_pk_to_url_str
from allauth.utils import build_absolute_uri
from dj_rest_auth.forms import AllAuthPasswordResetForm
from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import (ReadOnlyPasswordHashField,
                                       UserCreationForm)
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

User = get_user_model()

default_token_generator = EmailAwarePasswordResetTokenGenerator()


def validate_password(self):
    if len(self) < 8:
        raise ValidationError(
            _('Password requires minimum 8 characters.'),
            code='invalid',
        )
    if self.isalpha() or self.isdigit():
        raise ValidationError(
            _('Your password must contain at least one number, one letter, and/or special character.'),
            code='invalid',
        )


def validate_fullname(self):
    fullname = self.split()
    if len(fullname) <= 1:
        raise ValidationError(
            _('Kindly enter more than one name, please.'),
            code='invalid',
            params={'value': self},
        )
    for x in fullname:
        if len(x) < 2:
            raise ValidationError(
                _('Please enter your name correctly.'),
                code='invalid',
                params={'value': self},
            )


class UserForm(forms.Form):
    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(UserForm, self).__init__(*args, **kwargs)


class UserAdminCreationForm(UserCreationForm):

    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput,
        strip=True,
        validators=[validate_password],
    )

    name = forms.CharField(
        label=_("Full Name"),
        widget=forms.TextInput,
        strip=True,
        validators=[validate_fullname],
    )

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('name', 'email',)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if (User.objects.filter(email=email.casefold()).exists()):
            raise forms.ValidationError(
                _("This email address is already in use."))
        return email

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"].lower()
        user.name = self.cleaned_data["name"].title()
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        label=_("Password"),
        help_text=_(
            "Raw passwords are not stored, so there is no way to see this "
            "user's password, but you can change the password using "
            "<a href=\"{}\">this form</a>."
        ),
    )

    name = forms.CharField(
        label=_("Full Name"),
        widget=forms.TextInput,
        strip=True,
        validators=[validate_fullname],
    )

    class Meta:
        model = User
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related(
                'content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial.get('password')

    def clean_name(self):
        name = self.cleaned_data["name"].title()
        return name

    # def clean_email(self):
    #     if (User.objects.filter(email=self.cleaned_data.get("email").casefold()).exists()):
    #         raise forms.ValidationError(
    #             _("This email address is already in use."))
    #     email = self.cleaned_data["email"].lower()
    #     return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"].lower()
        user.name = self.cleaned_data["name"].title()
        if commit:
            user.save()
        return user


class CustomSetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class EmailConfirmationForm(UserForm):

    email = forms.EmailField(
        label=_("E-mail"),
        required=True,
        widget=forms.TextInput(
            attrs={"type": "email", "placeholder": _("E-mail address")}
        ),
    )

    def clean_email(self):
        value = self.cleaned_data["email"]
        value = self.clean_email(value)
        return value

    def save(self, request):
        return EmailAddress.objects.add_email(
            request, self.user, self.cleaned_data["email"], confirm=True
        )
        
class CustomPasswordResetForm(AllAuthPasswordResetForm):
    """
    We inherit the Original class of the allauth package to specify the 
    custom reset password template by overriding the save method since 
    there's no adapter to specify the default email template.
    """
    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:

            temp_key = token_generator.make_token(user)
            
            path = reverse(
                'password_reset_confirm',
                args=[user_pk_to_url_str(user), temp_key],
            )
            url = build_absolute_uri(request, path)

            context = {
                'current_site': current_site,
                'user': user,
                'password_reset_url': url,
                'request': request,
            }
            get_adapter(request).send_mail(
                'accounts/email/password_reset_key', email, context
            )
        return self.cleaned_data['email']


