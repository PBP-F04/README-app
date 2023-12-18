import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods
from .models import BookLoan
from KatalogBuku.models import Book
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from UserProfile.models import Profile
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt


@login_required
@csrf_exempt
@require_http_methods(["POST", "GET", "PATCH"])
def read_book(request):
    if request.method == "POST":
        user = request.user
        json_data = json.loads(request.body)
        book_id = json_data["book_id"]
        if book_id is None:
            return JsonResponse(
                {"status": 400, "message": "Book ID is empty"}, status=400
            )
        print(user.id)
        profile = Profile.objects.filter(user=user.id).first()
        if profile is None:
            return JsonResponse(
                {"status": 400, "message": "Profile not found"}, status=400
            )
        book = Book.objects.filter(id=book_id).first()
        if book is None:
            return JsonResponse(
                {"status": 400, "message": "Book not found"}, status=400
            )

        loan = BookLoan.objects.filter(user=profile, book=book).first()
        if loan is not None:
            return JsonResponse(
                {"status": 400, "message": "Book already borrowed"}, status=400
            )

        BookLoan.objects.create(user=profile, book=book, borrow_date=datetime.now())

        return JsonResponse(
            {"status": 200, "message": "success borrow book"}, status=200
        )
    elif request.method == "GET":
        user = request.user
        profile = Profile.objects.filter(user=user.id).first()
        if profile is None:
            return JsonResponse(
                {"status": 400, "message": "Profile not found"}, status=400
            )
        loans = (
            BookLoan.objects.filter(user=profile)
            .select_related("book")
            .values(
                "id",
                "book_id",
                "book__title",
                "book__book_code",
                "book__author",
                "borrow_date",
                "done_date",
                "status",
            )
        )
        data = []
        for loan in loans:
            print(loan)
            data.append(
                {
                    "loan_id": loan["id"],
                    "book_id": loan["book_id"],
                    "book_title": loan["book__title"],
                    "book_code": loan["book__book_code"],
                    "book_author": loan["book__author"],
                    "borrow_date": loan["borrow_date"],
                    "done_date": loan["done_date"],
                    "status": loan["status"],
                }
            )
        return JsonResponse(
            {"status": 200, "message": "success", "data": data}, status=200
        )
    elif request.method == "PATCH":
        user = request.user
        json_data = json.loads(request.body)
        loan_id = json_data["loan_id"]
        if loan_id is None:
            return JsonResponse(
                {"status": 400, "message": "loan ID is empty"}, status=400
            )
        profile = Profile.objects.filter(user=user.id).first()
        if profile is None:
            return JsonResponse(
                {"status": 400, "message": "Profile not found"}, status=400
            )
        loan = BookLoan.objects.filter(user=profile.id, id=loan_id).first()
        if loan is None:
            return JsonResponse(
                {"status": 400, "message": "Loan not found"}, status=400
            )

        if loan.status == "RETURNED":
            return JsonResponse(
                {"status": 400, "message": "Book already returned"}, status=400
            )
        loan.done_date = datetime.now()
        loan.status = "RETURNED"
        loan.save()
        return redirect('my_borrowed_books')  # Redirect to a page showing the user's borrowed books
