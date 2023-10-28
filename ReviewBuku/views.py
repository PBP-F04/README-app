from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login/')
def show_read_books(request):
    context = {

    }

    return render(request, 'read_books.html', context)

def review_buku(request):
    context = {

    }

    return render(request, 'review_buku.html', context)
