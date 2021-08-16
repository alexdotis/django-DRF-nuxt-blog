from dj_rest_auth.registration.serializers import ResendEmailVerificationSerializer
from allauth.account.models import EmailAddress
from rest_framework.permissions import  AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
from django.utils.translation import gettext_lazy as _
from rest_framework.response import Response

class ResendEmailVerificationView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = ResendEmailVerificationSerializer
    queryset = EmailAddress.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            email = EmailAddress.objects.get(**serializer.validated_data)
        except EmailAddress.DoesNotExist:
            raise ValidationError("Account does not exist")

        if email.verified:
            raise ValidationError("Account is already verified")

        email.send_confirmation()
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)