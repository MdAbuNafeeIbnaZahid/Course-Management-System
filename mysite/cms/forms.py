from django import forms
from cms.models import Student, User, Course, Class_of_course, Enrolment, Teacher, Department, Forum_post, Submission, Submission_window
import datetime, pytz
from pytz import timezone

from django.contrib.admin import widgets

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


class teacher_post_in_class_forum_form(forms.ModelForm) :
    class Meta:
        model = Forum_post
        fields = [ 'headline', 'text', 'document' ]


class teacher_set_mark_of_an_enrolment_form(forms.ModelForm) :
    class Meta:
        model = Enrolment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(teacher_set_mark_of_an_enrolment_form, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['class_of_course'].disabled = True
        self.fields['approval_status'].disabled = True


class student_see_mark_of_an_enrolment_form(forms.ModelForm) :
    class Meta:
        model = Enrolment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(student_see_mark_of_an_enrolment_form, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['class_of_course'].disabled = True
        self.fields['approval_status'].disabled = True
        self.fields['ct1_marks'].disabled = True
        self.fields['ct2_marks'].disabled = True
        self.fields['ct3_marks'].disabled = True
        self.fields['ct4_marks'].disabled = True
        self.fields['ct5_marks'].disabled = True
        self.fields['ct6_marks'].disabled = True
        self.fields['assignment1_marks'].disabled = True
        self.fields['assignment2_marks'].disabled = True
        self.fields['assignment3_marks'].disabled = True
        self.fields['attendance_marks'].disabled = True
        self.fields['term_final_marks'].disabled = True
        self.fields['viva1_marks'].disabled = True
        self.fields['viva2_marks'].disabled = True
        self.fields['experiment_marks'].disabled = True
        self.fields['other'].disabled = True
        self.fields['final_out_of_hundred'].disabled = True



# class Teacher_add_submission_window_form(forms.ModelForm) :
#     class Meta:
#         model = Submission_window
#         fields = '__all__'
#     #     # widgets = {
#     #     #     'end_time': forms.DateTimeBaseInput(),
#     #     #     # 'email_address' : forms.EmailField(),
#     #     # }
#     #
#     #
#
#     def __init__(self, *args, **kwargs):
#         super(Teacher_add_submission_window_form, self).__init__(*args, **kwargs)
#         self.fields['end_time'].label = 'End time (format 2006-10-25 14:30)'
#         self.fields['teacher'].disabled = True
#         self.fields['class_of_course'].disabled = True
#
#



class Teacher_add_submission_window_form(forms.Form) :
    headline = forms.CharField(min_length=1)
    body = forms.CharField(min_length=1, widget=forms.Textarea)
    end_time = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])


    def __init__(self, *args, **kwargs):
        super(Teacher_add_submission_window_form, self).__init__(*args, **kwargs)

    # def clean_end_time(self):
    #     print('inside clean_end_time')
    #     try:
    #         end_time = self.cleaned_data['end_time']
    #         localtz = timezone('Asia/Dhaka')
    #         end_time = localtz.localize(end_time)
    #
    #         if ( end_time < datetime.datetime.now() ):
    #             raise forms.ValidationError('Invalid date')
    #     except:
    #         raise forms.ValidationError('Invalid date')
    #
    #     return end_time


    # def clean(self):
    #     print('inside clean method of Teacher_add_submission_window_form')
    #     cleaned_data = super(Teacher_add_submission_window_form, self).clean()
    #
    #
    #     end_time = cleaned_data.get('end_time', None)
    #
    #     localtz = timezone('Asia/Dhaka')
    #     # end_time = localtz.localize( cleaned_data['end_time'] )
    #
    #
    #     if ( end_time < datetime.datetime.now() ) :
    #         print('raising form error...  end_time < datetime.datetime.now()   ')
    #         raise forms.ValidationError('Invalid date time')
    #
    #     self.cleaned_data['end_time'] = end_time
    #
    #
    #
    #     return self.cleaned_data






    # def clean(self):
    #     print('inside clean method of Teacher_add_submission_window_form')
    #     cleaned_data = super(Teacher_add_submission_window_form, self).clean()
    #
    #     try :
    #         end_time = cleaned_data.get('end_time', None)
    #         print('end_time = ' + str(end_time) )
    #         localtz = timezone('Asia/Dhaka')
    #         print('localtz = ' + str(localtz) )
    #
    #         print('end_time = ' + str(end_time) )
    #
    #         if ( end_time < timezone.now() ) :
    #             print('raising form error...  end_time < datetime.datetime.now()   ')
    #             raise forms.ValidationError('Invalid date time')
    #
    #         self.cleaned_data['end_time'] = end_time
    #
    #     except :
    #         print('raising form error....   in except')
    #         raise forms.ValidationError('Invalid date time')
    #
    #     return self.cleaned_data


class Student_edit_submission_form(forms.ModelForm):
    class Meta:
        model = Submission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(Student_edit_submission_form, self).__init__(*args, **kwargs)
        self.fields['student'].disabled = True
        self.fields['submission_window'].disabled = True


class User_change_password_form(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_again = forms.CharField(widget=forms.PasswordInput)


class User_update_profile_form(forms.ModelForm):
    class Meta:
        model = User
        #fields = '__all__'
        fields = ['first_name', 'last_name', 'address', 'phone_num', 'email_address']

    def __init__(self, *args, **kwargs):
        super(User_update_profile_form, self).__init__(*args, **kwargs)
