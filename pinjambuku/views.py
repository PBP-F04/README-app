from django.shortcuts import get_object_or_404, redirect, render
from .models import BookLoan
from KatalogBuku.models import Book
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404
from django.db.models import Q
#TODO: ajax, bootstrap

# Create your views here.
"""
Modul Pinjam Buku adalah fitur yang memungkinkan pengguna untuk mencari dan meminjam buku dari perpustakaan digital atau fisik. 
Pengguna dapat mencari buku berdasarkan judul, penulis, atau kategori, lalu meminjam buku tersebut untuk dibaca. 
Modul ini juga dapat melacak tenggat waktu pengembalian buku dan memberi pengguna akses ke buku yang telah mereka pinjam. 
Selain itu, modul pinjam buku juga mempertimbangkan stok buku yang dapat dipinjam sehingga 
stok yang dapat dipinjam habis maka pengguna tidak dapat meminjam buku jenis tersebut. 
Tentunya selain pengguna dapat meminjam buku, mereka juga bisa mengembalikan buku.
"""

@login_required
def track_return_date(request, loan_id):
    loan = get_object_or_404(BookLoan, id=loan_id, user=request.user)

    return render(request, 'track_return_date.html', {'loan': loan})

@login_required
def borrow_book(request):
    book = get_object_or_404(Book)

    if request.method == "POST":
        # Create a book loan record
        loan = BookLoan(user=request.user, book=book, borrow_date=timezone.now(), due_date=timezone.now() + timezone.timedelta(days=14))
        loan.save()
        return redirect('my_borrowed_books')  # Redirect to a page showing the user's borrowed books

    return render(request, 'borrow_book.html', {'book': book})

@login_required
def return_book(request, loan_id):
    loan = get_object_or_404(BookLoan, id=loan_id, user=request.user)

    if request.method == "POST":
        # Update the finished_date field to mark the book as returned
        loan.finished_date = timezone.now()
        loan.save()
        return redirect('my_borrowed_books')  # Redirect to a page showing the user's borrowed books

    return render(request, 'return_book.html', {'loan': loan})