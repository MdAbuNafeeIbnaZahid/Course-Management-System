from django.views.decorators.csrf import csrf_exempt



from django.urls import reverse

from django.shortcuts import render, redirect

from django.http import HttpResponse, Http404
import datetime
from random import randint
from django.template.loader import get_template
from django.template import Context, Template
from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from books.models import Book
from mysite.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail

from cms.models import Teacher, Student, User, Department
from cms.templates import includes
from cms.forms import Student_profile_form, add_new_student_form







# Create your views here.

@csrf_exempt
def handle_log_in(request, **kwargs):

    print("beginning of handle_log_in")

    current_username = request.session.get( 'username', None )

    print('current_username = ' + str(current_username) )

    if ( current_username is not None ): # user already logged in
        current_user = User.objects.get(username= current_username )
        if ( current_user.user_type == 'ADMIN' ) :
            return render(request, 'admin_homepage.html', { 'username' : current_username } )
        elif ( current_user.user_type == 'TEACHER' ) :
            return render(request, 'teacher_homepage.html', {'username': current_username})
        elif (current_user.user_type == 'STUDENT') :
            return render(request, 'student_homepage.html', {'username': current_username} )

    else: # user not logged in
        if request.method == 'POST' : # one has clicked the login button

            print( 'one has clicked the log in button' )

            username = request.POST.get('username', None)

            print("username = " + username)

            password = request.POST.get('password', None)

            print('password = ' + password)

            try:
                user = User.objects.get( username= username )
            except User.DoesNotExist:
                user = None

            if (user is None or user.password != password): # incorrect username or password
                return render(request, 'login_page.html', {'error': 'Wrong username or password'} )

            else: # correct username and password
                request.session['username'] = username
                request.session['user_type'] = user.user_type
                return HttpResponseRedirect( reverse('handle_log_in' )  );

        else:  # one has just loaded the page
            return render(request, 'login_page.html', {'error': None} )


def handle_update_profile(request):
    current_username = request.session.get('username', None)
    if (current_username is None): #user not logged in
        return render(request, 'login_page.html', {'error': None})
    else:
        return render(request, 'user_navigation.html', {'error': None})


def handle_change_password(request):
    current_username = request.session.get('username', None)
    if (current_username is None):  # user not logged in
        return render(request, 'login_page.html', {'error': None})
    else:
        return render(request, 'user_navigation.html', {'error': None})


def handle_log_out(request):
    request.session['username'] = None
    request.session['usertype'] = None
    return redirect( handle_log_in )
    # return render(request, 'login_page.html', {'error' : False} )


def change_profile_student(request):
    username = request.session.get('username', '')
    student = Student.objects.get(username=username)
    student_profile_form = Student_profile_form(request.POST ,instance=student)
    if student_profile_form.is_valid():
        student_profile_form.save()
    return render(request, 'student_profile_update.html', {'student_profile_form' : student_profile_form})


def handle_add_department(request):
    user_type = request.session.get('user_type', None)
    print('user_type = ' + user_type)
    if user_type == 'ADMIN' : # user is admin

        dept_list = Department.objects.all()

        if request.method == 'POST' : # clicked add button
            department_name = request.POST.get( 'department_name', None )
            same_name_dept_cnt = Department.objects.all().filter( name=department_name ).count()
            if ( same_name_dept_cnt > 0):
                return render(request, 'add_new_department.html', {'error' : 'Dept already exists', 'dept_list' : dept_list} )
            else:
                dept = Department(name=department_name)
                dept.save()
                return render(request, 'add_new_department.html', {'dept_list': dept_list, 'success_message' : 'dept added successfully'} )

        else: # admin just loaded the page
            return render(request, 'add_new_department.html', { 'dept_list' : dept_list } )
    else: # Non admin
        print('user is not admin')
        return render(request, 'includes/user_navigation.html', {'error': None})



def handle_add_new_student(request):
    user_type = request.session.get('user_type', None)
    if ( user_type != 'ADMIN' ): # Non admin
        print('User is not admin')
        return render( request, 'includes/user_navigation.html', {'error': None} )

    else: #user is admin

        if ( request.method == 'POST' ) : #user clicked on the add button

            print('user clicked on the add button')

            form = add_new_student_form(request.POST)



            if ( form.is_valid() ) :

                print( ' form is valid ' )

                username =  form.cleaned_data.get('username', None)

                print( 'username = ' + username )


                password = form.cleaned_data.get('password', None )
                student_id = form.cleaned_data.get( 'studentId', None )
                dept = form.cleaned_data.get('dept', None)
                level = form.cleaned_data.get('level', None)
                term = form.cleaned_data.get( 'term', None )

                user_with_same_username_cnt = User.objects.filter(username= username).count()

                if ( user_with_same_username_cnt > 0 ):
                    return render(request, 'add_new_student.html',
                                  {'add_new_student_form': form, 'error' : 'username already exists'} )

                student_with_same_std_id_cnt = Student.objects.filter( studentId= student_id ).count()

                if ( student_with_same_std_id_cnt > 0 ) :
                    return render(request, 'add_new_student.html',
                                  {'add_new_student_form': form, 'error': 'student id already exists'} )


                student_to_add = form.save(commit=False)
                student_to_add.user_type = 'STUDENT'

                student_to_add.save()

                return render(request, 'add_new_student.html',
                              {'add_new_student_form': form,
                                'message' : 'successfully added student' })


            else: # form is not valid
                return render(request, 'add_new_student.html',
                              {'add_new_student_form': form, 'error': 'form is invalid'})

        else: # user just loaded the page
            form = add_new_student_form()
            return render(request, 'add_new_student.html',
                          { 'add_new_student_form' : form } )

# def handle_log_in(request, logged_out = False ):
#     if logged_out:
#         return render(request, 'login_page.html', {'error': False})
#
#     username = request.session.get('username', '')
#     usertype = request.session.get('usertype', '')
#     if (username != '' and usertype != ''):
#         if ( usertype == 'teacher' ):
#             return render(request, 'teacher_homepage.html')
#
#         elif (usertype == 'student'):
#             return render(request, 'student_homepage.html')
#
#
#     username = request.GET.get('username', '')
#     password = request.GET.get('password', '')
#     usertype = request.GET.get('usertype', '')
#
#     # print(username)
#     # print(password)
#     # print(usertype)
#
#     if ( usertype == "teacher" ):
#         teacher = Teacher.objects.filter(username=username, password=password)
#         print(teacher)
#         if teacher:
#             print("teacher found")
#             request.session['username'] = username
#             request.session['usertype'] = usertype
#             return render(request, 'teacher_homepage.html')
#         else:
#             print("Teacher not found")
#
#     elif ( usertype == 'student' ):
#         student = Student.objects.filter(username=username, password=password)
#         print(student)
#         if student:
#             print("student found")
#             request.session['username'] = username
#             request.session['usertype'] = usertype
#             return render(request, 'student_homepage.html')
#         else:
#             print("student not found")
#
#     return render(request, 'login_page.html', {'error' : True} )
