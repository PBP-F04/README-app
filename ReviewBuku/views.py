from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest, JsonResponse
from UserProfile.models import Profile

from KatalogBuku.models import Book
from ReviewBuku.forms import ReviewForm
from .models import BookReview, UpvotedReview
from pinjambuku.models import BookLoan

@login_required(login_url='/login/')
def show_page_review(request, book_id):
    book = Book.objects.get(id=book_id)

    book_reviews = BookReview.objects.filter(book=book)

    # upvoted_reviews = UpvotedReview.objects.filter(book=book)

    context = {
        'book': book,
        'book_reviews': book_reviews,
        # 'upvoted_reviews' if needed
    }

    return render(request, 'show_page_review.html', context)

@login_required(login_url='/login/')
def review_buku(request, book_id):
    book = Book.objects.get(id=book_id)
    user = request.user
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        profile = Profile.objects.filter(user=user.id).first()
        if form.is_valid():  
            book_review = form.save(commit=False)
            book_review.user = profile
            book_review.book = book
            book_review.save()

            return redirect(reverse('ReviewBuku:show_page_review_ajax', args=[book_id]))
        else:
            return HttpResponseBadRequest("Invalid form data")

    else:
        form = ReviewForm() 

    context = {
        'book_id': book_id,
        'form': form, 
    }

    return render(request, 'review_buku.html', context)

@login_required(login_url='/login/')
@csrf_exempt
def show_page_review_ajax(request, book_id):
    book = Book.objects.get(id=book_id)
    book_reviews = BookReview.objects.filter(book=book)

    review_data = []
    for review in book_reviews:
        review_data.append({
            'id': str(review.id),
            'user': review.user.username,
            'review_score': review.review_score,
            'review_content': review.review_content,
            'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        })

    if request.method == 'POST':
        return JsonResponse({'reviews': review_data})
    
    response = {
        "book" : book
    }
    print(response)
    return render(request, 'page_review.html', response)

@login_required(login_url='/login/')
@csrf_exempt
def show_page_review_user_ajax(request):
    user = request.user
    profile = Profile.objects.filter(user=user.id).first()
    book_reviews = BookReview.objects.filter(user=profile).all()
    review_data = []


    for review in book_reviews:
            review_data.append({
                'id': str(review.id),
                'user': review.user.username,
                'review_score': review.review_score,
                'review_content': review.review_content,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            })
    
    if request.method == 'POST':
        return JsonResponse({'reviews': review_data})
    
    response = {
        "profile" : profile
    }
    print(response)
    return render(request, 'page_review.html', response)

    
   
