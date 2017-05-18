from django import forms
from cms.models import Student, User, Course, Class_of_course, Enrolment, Teacher, Department

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


class add_new_teacher_form(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['username', 'password', 'dept', 'rank']
        widgets = {
            'password': forms.PasswordInput(),
            # 'email_address' : forms.EmailField(),
        }


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



class admin_set_dept_head_form(forms.Form):
    dept = forms.ModelChoiceField( Department.objects.all() )
    head = forms.ModelChoiceField( Teacher.objects.all().order_by( 'dept' ) )

    def clean(self):

        # clean method is never called
        # I don't know why it is happening

        dept_ = self.cleaned_data.get('dept', None)
        head_ = self.cleaned_data.get('head', None)
        print('dept = ' + dept_ )
        print( 'head = ' + head_ )

        # raise ValidationError('Form is not valid')

        return self.cleaned_data


class hod_approve_enrolment_form(forms.Form) :
    enrolments_to_deal = forms.ModelMultipleChoiceField(queryset=None, \
                    widget=forms.CheckboxSelectMultiple)
    def __init__(self, dept, *args, **kwargs):
        super(hod_approve_enrolment_form, self).__init__(*args, **kwargs)
        all_waiting_for_approval_enrolment_of_this_dept = Enrolment.objects.all().\
            filter(approval_status=Enrolment.WAITING_FOR_APPROVAL, student__dept=dept).order_by(
            'student__studentId')
        self.fields[ 'enrolments_to_deal' ].queryset = all_waiting_for_approval_enrolment_of_this_dept