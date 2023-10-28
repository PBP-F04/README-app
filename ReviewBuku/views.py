from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from KatalogBuku.models import Book
from .models import BookReview, UpvotedReview
from pinjambuku.models import bookloans

@login_required(login_url='/login/')
def show_read_books(request):
    # Get the user's read books (imported from bookloans)
    read_books = bookloans.objects.filter(user=request.user, returned=True)  # Assuming "returned" is a field that indicates if a book has been returned

    context = {
        'read_books': read_books,
    }

    return render(request, 'read_books.html', context)

@login_required(login_url='/login/')
def review_buku(request, book_id):
    # Handle book review submission
    if request.method == 'POST':
        user = request.user
        book = Book.objects.get(id=book_id)  # Assuming you pass the book_id when the user wants to review a specific book
        review_score = float(request.POST.get('review_score'))
        review_content = request.POST.get('review_content')

        # Create a new BookReview instance
        BookReview.objects.create(user=user, book=book, review_score=review_score, review_content=review_content)

        return redirect('show_read_books')  # Redirect to the read books page after submitting the review

    # This is a GET request; show the review form
    context = {
        'book_id': book_id,
    }

    return render(request, 'review_buku.html', context)

