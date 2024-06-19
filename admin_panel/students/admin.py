from django.contrib import admin

from students.models import Student, StudentsMarks


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ('name', 'class_name')
    list_display = ('name', 'class_name', 'age')
    list_filter = ('name', 'class_name', 'age')


@admin.register(StudentsMarks)
class MarksAdmin(admin.ModelAdmin):
    search_fields = ('student', 'subject')
    list_display = ('student', 'subject', 'mark', 'created_at')
    list_filter = ('student', 'subject', 'mark')
