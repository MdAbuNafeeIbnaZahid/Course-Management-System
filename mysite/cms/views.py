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

from cms.models import Teacher, Student
from cms.templates import includes
from cms.forms import Student_profile_form


# Create your views here.

def handle_log_in(request, logged_out = False ):
    if logged_out:
        return render(request, 'login_page.html', {'error': False})

    username = request.session.get('username', '')
    usertype = request.session.get('usertype', '')
    if (username != '' and usertype != ''):
        if ( usertype == 'teacher' ):
            return render(request, 'teacher_homepage.html')

        elif (usertype == 'student'):
            return render(request, 'student_homepage.html')


    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    usertype = request.GET.get('usertype', '')

    # print(username)
    # print(password)
    # print(usertype)

    if ( usertype == "teacher" ):
        teacher = Teacher.objects.filter(username=username, password=password)
        print(teacher)
        if teacher:
            print("teacher found")
            request.session['username'] = username
            request.session['usertype'] = usertype
            return render(request, 'teacher_homepage.html')
        else:
            print("Teacher not found")

    elif ( usertype == 'student' ):
        student = Student.objects.filter(username=username, password=password)
        print(student)
        if student:
            print("student found")
            request.session['username'] = username
            request.session['usertype'] = usertype
            return render(request, 'student_homepage.html')
        else:
            print("student not found")

    return render(request, 'login_page.html', {'error' : True} )



def handle_log_out(request):
    request.session['username'] = ''
    request.session['usertype'] = ''
    return redirect( handle_log_in )
    # return render(request, 'login_page.html', {'error' : False} )


def change_profile_student(request):
    username = request.session.get('username', '')
    student = Student.objects.get(username=username)
    student_profile_form = Student_profile_form(request.POST ,instance=student)
    if student_profile_form.is_valid():
        student_profile_form.save()
    return render(request, 'student_profile_update.html', {'student_profile_form' : student_profile_form})




