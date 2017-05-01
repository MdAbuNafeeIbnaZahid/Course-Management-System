from django.shortcuts import render

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


# Create your views here.

def handle_log_in(request):
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
            # return render(request, 'teacher_navigation.html')
            request.session['username'] = username
            request.session['usertype'] = usertype
        else:
            print("Teacher not found")

    elif ( usertype == 'student' ):
        student = Student.objects.filter(username=username, password=password)
        print(student)
        if student:
            print("student found")
            request.session['username'] = username
            request.session['usertype'] = usertype
            # return render(request, 'student_navigation.html')
        else:
            print("student not found")

    return render(request, 'login_page.html')


