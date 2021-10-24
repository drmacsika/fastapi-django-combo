from core.settings import DRF_V1_STR
from dj_rest_auth.registration.views import ConfirmEmailView, VerifyEmailView
from django.urls import path
from django.urls.conf import include, path

from .views import (CustomEmailConfirmationView, CustomLoginView,
                    CustomPasswordResetView, CustomPasswordSetView,
                    CustomRegisterView)

app_name = "accounts"

urlpatterns = [
    path("accounts/", include('dj_rest_auth.urls')),
    # The confirm_email path below should always be placed 
    # above the signup view otherwise there will be a template error
    path("accounts/confirm-email/<str:key>/",
        ConfirmEmailView.as_view(), name='confirm_email',
    ),
    path("accounts/signin/",
         CustomLoginView.as_view(), name="login"),
    path("accounts/password/reset/", CustomPasswordResetView.as_view(),
         name='password_reset'),
    path("accounts/password/set/",
         CustomPasswordSetView.as_view(), name="set_password"),
    path(f"accounts/signup/", CustomRegisterView.as_view(),
         name='signup'),
    path("accounts/confirm-email/", VerifyEmailView.as_view(),
         name='email_verification_sent'),
    path("accounts/resend-email/",
         CustomEmailConfirmationView.as_view(), name="resend_email"),

]



