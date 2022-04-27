from rest_framework import serializers
from .models import Router

class RouterSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for Router"""
    class Meta:
        model = Router
        fields = ['id','sap_id', 'hostname', 'loopback', 'mac_address', 'created_at', 'updated_at', 'deleted_at']