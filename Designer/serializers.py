from rest_framework import serializers
from .models import styleDB

class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = styleDB
        fields = '__all__'