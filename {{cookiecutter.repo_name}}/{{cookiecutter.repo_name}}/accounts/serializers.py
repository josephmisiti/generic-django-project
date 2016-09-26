import logging

from rest_framework import serializers

logger = logging.getLogger(__name__)

class UserSerializer(serializers.ModelSerializer):
        
    class Meta:
        model = User
