from rest_framework import serializers
from .models import School

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        # This includes all fields from your School model
        fields = '__all__'
        fields = [
        "name", "type", "address", "city", "state", "zipcode", "id", 
        "test_scores_required", "latest.admissions.admission_rate.overall", "tuition", "living_expenses", 
        "number_of_student", "staff_student_rate", "gar", 
        "climate", "courses_and_classes", "deadline_dates", 
        "scholarship", "school_url", "english_proficiency_required"
        ]