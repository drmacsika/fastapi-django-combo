from accounts.views import CustomPasswordResetConfirmView
from django.contrib import admin
from django.urls import path
from django.urls.conf import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from core.settings import DRF_V1_STR

urlpatterns = [

    # Simple JWT
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    path("token/verify/", TokenVerifyView.as_view()),

    # rest_framework
    path("", include('rest_framework.urls')),

    # The pasword reset path below can only work
    # if added to the high level urls.py file
    path(
        "accounts/password/reset/<slug:uidb64>/<slug:token>/",
        CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'
    ),
    path("", include("accounts.urls")),
    path('admin/', admin.site.urls),
]
