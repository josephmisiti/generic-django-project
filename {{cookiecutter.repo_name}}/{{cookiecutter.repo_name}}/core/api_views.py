from django.shortcuts import get_object_or_404

from rest_framework import (
    filters,
    status,
    mixins,
    viewsets,
    generics
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny,
    IsAdminUser,
    IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from . import constants
from . import models
from . import serializers

#class TimeSlotAPIView(viewsets.ModelViewSet):
#    permission_classes = (IsAuthenticated,)
#    #authentication_classes = (NoCSRFSessionAuthentication,)
#    queryset = models.ProducingAgentLicense.objects.all()
#    serializer_class = serializers.ProducingAgentLicenseSerializer
