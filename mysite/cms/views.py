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


# Create your views here.

def handle_log_in(request):
    username = request.GET.get('username', '')
    password = request.GET.get('password', '')
    usertype = request.GET.get('usertype', '')

    # print(username)
    # print(password)
    # print(usertype)

    if ( usertype == "teacher" ):
        teacher = Teacher.objects.filter(username=username)
        print(teacher)
        pass

    elif ( usertype == 'student' ):
        student = Student.objects.filter(username=username)
        print(student)
        pass

    return render(request, 'login_page.html')


