from django import forms
from cms.models import Student

class Student_profile_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['password', 'first_name', 'last_name', 'address', 'division', 'phone_num', 'email_address', ]
        widgets = {
            'password' : forms.PasswordInput(),
            # 'email_address' : forms.EmailField(),
        }