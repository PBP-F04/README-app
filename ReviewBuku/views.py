from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from KatalogBuku.models import Book
from ReviewBuku.forms import ReviewForm
from .models import BookReview, UpvotedReview
from pinjambuku.models import BookLoan

@login_required(login_url='/login/')
def show_read_books(request):
    # Get the user's read books (imported from bookloans)
    read_books = BookLoan.objects.filter(user=request.user, returned=True)  

    context = {
        'read_books': read_books,
    }

    return render(request, 'read_books.html', context)

@login_required(login_url='/login/')
def review_buku(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():  
            book_review = form.save(commit=False)
            book_review.user = request.user
            book_review.book = book
            book_review.save()

            return redirect('show_read_books')

    else:
        form = ReviewForm() 

    context = {
        'book_id': book_id,
        'form': form, 
    }

    return render(request, 'review_buku.html', context)


@csrf_exempt
def show_read_books_ajax(request):
    if request.method == 'POST':
        read_reviews = BookReview.objects.filter(user=request.user)

        reviews_data = []
        for review in read_reviews:
            reviews_data.append({
                'book_title': review.book.title,
                'review_score': review.review_score,
                'review_content': review.review_content,
            })

        return JsonResponse({'reviews': reviews_data})
    else:
        return JsonResponse({'error': 'Invalid request method'})


