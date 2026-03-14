from rest_framework import serializers
from .models import School, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        # This includes all fields from your School model
        fields = '__all__'