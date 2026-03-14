from django.contrib import admin
from .models import User, CostOfAttendance, School

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # It is safer to exclude the password from the list view
    list_display = ('username', 'email') 

class CostOfAttendanceInline(admin.StackedInline):
    model = CostOfAttendance
    can_delete = False
    verbose_name_plural = 'Cost of Attendance'

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    inlines = [CostOfAttendanceInline]