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


def hello(request):
    print("request.path = " + request.path)
    print("request.get_host() = " + request.get_host() );
    print("request.get_full_path() = " + request.get_full_path() );
    print("request.is_secure() = " + str( request.is_secure() ) );
    httpResponseStr = "Welcome to the page at {}".format( request.path + "" );
    print(  httpResponseStr  )
    return  HttpResponse( httpResponseStr  )

def my_homepage_view(request):
    return  HttpResponse("homepage")

def default_view(request):
    return  HttpResponse("default")

def current_datetime(request):
    now = datetime.datetime.now()
    return render(request, 'dateapp/current_datetime.html', {'current_date' : now})

def hours_ahead(request, offset_hour, offset_minute):
    try:
        offset_hour = int(offset_hour)
        offset_minute = int(offset_minute)
    except ValueError:
        raise Http404()
    now = datetime.datetime.now()
    assert False
    dt = now + datetime.timedelta(hours=offset_hour, minutes=offset_minute)
    html = "{} is now {} ".format('time', now) + '<br>'
    html += "it will be {}".format(dt)
    return HttpResponse(html)

def ua_display_good2(request):
    ua = request.META.get('HTTP_USER_AGENT', 'unknown')
    return HttpResponse("Ur browser is {}".format(ua) )


def display_meta(request):
    values = request.META.items()

    html = []
    for k, v in values:
        html.append( '  <tr> <td> {} </td> <td> {} </td> </tr>  '.format(k, v) )
    return HttpResponse( ' <table> {} </table> '.format( '\n'.join( html ) ) );



def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'),
                ['siteowner@example.com']
            )
            return HttpResponseRedirect('/contact/thanks/')
    else:
        form = ContactForm(
            initial={'subject' : 'I love ur site'}
        )
    return render(request, 'contact_form.html', {'form' : form})