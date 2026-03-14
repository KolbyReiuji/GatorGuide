from django.db import models

class CostOfAttendance(models.Model):
    tuition = models.DecimalField(max_digits=12, decimal_places=2)
    living_expenses = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Tuition: {self.tuition}, Living: {self.living_expenses}"

class School(models.Model):
    # Basic Info
    name = models.CharField(max_length=255)
    school_type = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=20)
    
    # Unique Identifier
    school_id = models.CharField(max_length=100, unique=True)
    
    # Requirements
    test_scores_required = models.CharField(max_length=255, help_text="SAT/ACT requirements")
    english_proficiency_required = models.CharField(max_length=255, help_text="e.g. TOEFL 90+, IELTS 7.0")
    
    # Academics & Stats
    number_of_students = models.PositiveIntegerField()
    staff_student_rate = models.CharField(max_length=50, help_text="e.g. 1:15")
    gar = models.CharField(max_length=50, verbose_name="Graduation Acceptance Rate")
    
    # Nested Object (Relationship)
    cost_of_attendance = models.OneToOneField(
        CostOfAttendance, 
        on_delete=models.CASCADE,
        related_name='school_details'
    )
    
    # Miscellaneous
    climate = models.CharField(max_length=255)
    courses_and_classes = models.TextField()
    deadline_dates = models.TextField()
    scholarship_info = models.TextField()
    school_url = models.URLField(max_length=500)

    def __str__(self):
        return self.name