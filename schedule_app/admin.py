from django.contrib import admin
from .models import Teacher, Group, Classroom, Subject, Schedule

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'middle_name', 'email')
    search_fields = ('last_name', 'first_name', 'email')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'faculty')
    search_fields = ('name', 'faculty')

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('number', 'building', 'capacity')
    search_fields = ('number', 'building')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'timeslot', 'subject', 'teacher', 'group', 'classroom', 'week_type')
    list_filter = ('day_of_week', 'week_type', 'group', 'teacher')
    search_fields = ('subject__name', 'teacher__last_name', 'group__name')
