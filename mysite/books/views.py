from django.shortcuts import render
from django.http import HttpResponse
from books.models import Book
from mysite.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.mail import send_mail


# Create your views here.



def search(request):
    error = False
    if ('q' in request.GET):
        if (len(request.GET['q'] ) > 0):
            q = request.GET[ 'q' ]
            books = Book.objects.filter(title__icontains=q)
            return render(request, 'search_results.html', {'books':books, 'query' : q})
        else:
            error = True
    return render(request, 'search_form.html', {'error' : error})



