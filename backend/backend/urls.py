from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from core.rest_settings.rest_view import ResendEmailVerificationView
from dj_rest_auth.registration.views import VerifyEmailView
from rest_auth.views import PasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('core.urls')),
    path('password-reset/confirm/<uid>/<token>',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('rest-auth/account-confirm-email/', VerifyEmailView.as_view(),
         name='account_email_verification_sent'),

    path('rest-auth/registration/resend-email/',
         ResendEmailVerificationView.as_view()),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls'))
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
