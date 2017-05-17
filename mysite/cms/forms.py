from django import forms
from cms.models import Student, User, Course, Class_of_course, Enrolment

class Student_profile_form(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['password', 'first_name', 'last_name', 'address', 'division', 'phone_num', 'email_address', ]
        widgets = {
            'password' : forms.PasswordInput(),
            # 'email_address' : forms.EmailField(),
        }


class add_new_user_form( forms.ModelForm ):
    class Meta:
        model = User
        fields = [ 'username', 'password',  ]

#
# class add_new_student_form( forms.ModelForm ):
#     username = forms.CharField(max_length=200)
#     password = forms.CharField( widget= forms.PasswordInput ),
#     student_id = forms.IntegerField(  )

class add_new_student_form( forms.ModelForm ) :
    class Meta:
        model = Student
        fields = [ 'username', 'password', 'studentId', 'dept', 'level', 'term' ]
        widgets = {
            'password': forms.PasswordInput(),
            # 'email_address' : forms.EmailField(),
        }

    # def clean(self):
    #     cleaned_data = super(add_new_student_form, self).clean()
    #     username =  cleaned_data.get('username', None )
    #     print( "username = " + username )


class add_new_course_form( forms.ModelForm ) :
    class Meta:
        model = Course
        fields = '__all__'



class add_new_class_of_course_form(forms.ModelForm):
    class Meta:
        model = Class_of_course
        fields = '__all__'


class student_enrol_in_class_form(forms.ModelForm):
    class Meta:
        model = Enrolment
        fields = [ 'class_of_course' ]

