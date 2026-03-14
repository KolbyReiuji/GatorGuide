from rest_framework import serializers
from .models import School, User, CostOfAttendance

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# Create this new serializer so we can nest it
class CostOfAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CostOfAttendance
        fields = ['tuition', 'living_expenses']

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'
    # Manually add the field back using the 'related_name' we set in models.py
    cost_of_attendance = CostOfAttendanceSerializer(read_only=True)