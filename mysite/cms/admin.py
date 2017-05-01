from django.contrib import admin
from django.forms import ModelForm, PasswordInput
from .models import Department, Teacher, Student, Course, Class_of_course, \
    Enrolment, Question_of_vote, Option_of_vote, Response_of_vote


class StudentAdminForm(ModelForm):
    class Meta:
        model = Student
        widgets = {
            'password' : PasswordInput(),
        }
        fields = "__all__"


class TeacherAdminForm(ModelForm):
    class Meta:
        model = Teacher
        widgets = {
            'password' : PasswordInput(),
        }
        fields = "__all__"


class StudentAdmin(admin.ModelAdmin):
    form = StudentAdminForm


class TeacherAdmin(admin.ModelAdmin):
    form = TeacherAdminForm

# Register your models here.

admin.site.register( Department )
admin.site.register( Teacher, TeacherAdmin )
admin.site.register( Student, StudentAdmin )
admin.site.register( Course )
admin.site.register( Class_of_course )
admin.site.register( Enrolment )
admin.site.register( Question_of_vote )
admin.site.register( Option_of_vote )
admin.site.register( Response_of_vote )
