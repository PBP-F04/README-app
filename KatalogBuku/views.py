import datetime
from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Book, Category, BookLike, RequestedBook
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from UserProfile.models import Profile
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from .forms import RequestedBookForm
from authentication.views import login_required_json


@require_http_methods(["GET"])
def index(request):
    user = request.user
    response = {"user": user}
    return render(request, "katalog.html", response)


@require_http_methods(["GET"])
def get_books(request):
    category = request.GET.get("category", None)
    sort = request.GET.get("sort", None)
    order = request.GET.get("order", None)
    page = request.GET.get("page", 1)
    search = request.GET.get("search", None)
    items_per_page = 20

    # Define allowed sort fields
    allowed_sort = ["issued", "title", "author", "subject", "category"]

    # Validate sort field
    if sort not in allowed_sort:
        sort = None

    # Validate order field
    if order not in ["asc", "desc"]:
        order = None

    # If sort field is defined, append order to it
    if sort is not None and order is not None:
        sort = f"{'' if order == 'asc' else '-'}{sort}"

    # Create a Q object for search
    search_query = Q(title__icontains=search) if search else Q()

    # Create a Q object for category
    category_query = Q(category__category_name=category) if category else Q()

    # Fetch books from the database
    books = (
        Book.objects.select_related("Category")
        .values(
            "id",
            "issued",
            "book_code",
            "title",
            "author",
            "book_read_url",
            "subject",
            "synopsis",
            "category__category_name",
        )
        .filter(search_query & category_query)
        .order_by(sort or "book_code")
    )

    # Paginate the results
    paginator = Paginator(books, items_per_page)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    books_list = list(books)

    response = {
        "status": 200,
        "message": "success",
        "data": books_list,
        "pagination": {
            "current_page": books.number,
            "total_page": books.paginator.num_pages,
            "has_previous": books.has_previous(),
            "has_next": books.has_next(),
        },
    }
    return JsonResponse(response, status=200)


@require_http_methods(["GET"])
def get_categories(request):
    categories = Category.objects.values("id", "category_name").all()
    categories = list(categories)
    for category in categories:
        category["id"] = str(category["id"])

    response = {"status": 200, "message": "success", "data": categories}
    return HttpResponse(
        json.dumps(response), content_type="application/json", status=200
    )


@require_http_methods(["GET"])
@login_required_json
def get_book_by_id_json(request, book_id):
    try:
        user = request.user
        profile = Profile.objects.filter(user=user.id).first()
        if profile is None:
            return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)
        book = (
            Book.objects.filter(id=book_id)
            .values(
                "id",
                "issued",
                "book_code",
                "title",
                "author",
                "book_read_url",
                "subject",
                "synopsis",
                "category__category_name",
            )
            .first()
        )
        if book is None:
            return JsonResponse(
                {"status": 404, "message": "Book not found"}, status=404
            )
        book["id"] = str(book["id"])
        book["category"] = book["category__category_name"]
        issued = book["issued"].split("-")
        issued = datetime.date(int(issued[0]), int(issued[1]), int(issued[2]))
        book["issued"] = issued.strftime("%d %B %Y")
        del book["category__category_name"]
        return JsonResponse(
            {"status": 200, "message": "success", "data": book}, status=200
        )

    except ValidationError as e:
        response = {
            "status": 400,
            "message": "Bad Request",
        }
        return JsonResponse(response, status=400)


@require_http_methods(["GET"])
@login_required(login_url="authentication:login")
def get_book_by_id(request, book_id):
    try:
        user = request.user
        profile = Profile.objects.filter(user=user.id).first()
        if profile is None:
            return HttpResponseRedirect(reverse("UserProfile:create_profile"))
        book = (
            Book.objects.filter(id=book_id)
            .values(
                "id",
                "issued",
                "book_code",
                "title",
                "author",
                "book_read_url",
                "subject",
                "synopsis",
                "category__category_name",
            )
            .first()
        )
        if book is None:
            response = {
                "status": 404,
                "message": "Book not found",
            }
            return HttpResponseRedirect(reverse("KatalogBuku:index"))
        book_like = BookLike.objects.filter(book=book["id"], user=profile).first()
        if book_like is None:
            book["is_liked"] = False
        else:
            book["is_liked"] = True

        book["id"] = str(book["id"])
        book["category"] = book["category__category_name"]
        issued = book["issued"].split("-")
        issued = datetime.date(int(issued[0]), int(issued[1]), int(issued[2]))
        book["issued"] = issued.strftime("%d %B %Y")
        del book["category__category_name"]

        book_like = BookLike.objects.filter(book=book["id"]).count()
        book["like"] = book_like
        response = {"status": 200, "message": "success", "data": book}
        return render(request, "detail-book.html", response)
    except ValidationError as e:
        response = {
            "status": 400,
            "message": "Bad Request",
        }
        return HttpResponseRedirect(reverse("KatalogBuku:index"))


@require_http_methods(["POST", "DELETE"])
@login_required()
@csrf_exempt
def like_book(request, book_id):
    user = request.user
    book = Book.objects.filter(id=book_id).first()
    profile = Profile.objects.filter(user=user.id).first()
    if book is None:
        response = {
            "status": 404,
            "message": "Book not found",
        }
        return HttpResponse(
            json.dumps(response), content_type="application/json", status=404
        )
    if request.method == "POST":
        book_like = BookLike.objects.filter(book=book, user=profile).first()
        if book_like is None:
            BookLike.objects.create(book=book, user=profile)
            response = {
                "status": 200,
                "message": "success",
            }
            return HttpResponse(
                json.dumps(response), content_type="application/json", status=200
            )
        else:
            response = {
                "status": 400,
                "message": "Book already liked",
            }
            return HttpResponse(
                json.dumps(response), content_type="application/json", status=400
            )
    if request.method == "DELETE":
        book_like = BookLike.objects.filter(book=book, user=profile).first()
        if book_like is None:
            response = {
                "status": 400,
                "message": "Book not liked",
            }
            return HttpResponse(
                json.dumps(response), content_type="application/json", status=400
            )
        else:
            book_like.delete()
            response = {
                "status": 200,
                "message": "success",
            }
            return HttpResponse(
                json.dumps(response), content_type="application/json", status=200
            )


@csrf_exempt
def unlike_book(request, book_id):
    user = request.user
    book = Book.objects.filter(id=book_id).first()
    profile = Profile.objects.filter(user=user.id).first()
    if book is None:
        response = {
            "status": 404,
            "message": "Book not found",
        }
        return HttpResponse(
            json.dumps(response), content_type="application/json", status=404
        )
    book_like = BookLike.objects.filter(book=book, user=profile).first()
    if book_like is None:
        response = {
            "status": 400,
            "message": "Book not liked",
        }
        return HttpResponse(
            json.dumps(response), content_type="application/json", status=400
        )
    else:
        book_like.delete()
        response = {
            "status": 200,
            "message": "success",
        }
        return HttpResponse(
            json.dumps(response), content_type="application/json", status=200
        )


@require_http_methods(["GET"])
@login_required(login_url="authentication:login")
def show_request_book(request):
    user = request.user
    profile = Profile.objects.filter(user=user.id).first()
    requests = RequestedBook.objects.values(
        "id", "title", "author", "reason", "user__username"
    ).all()
    response = {"profile": profile, "requests": requests}
    return render(request, "request_book.html", response)


@login_required(login_url="authentication:login")
def form_request_book(request):
    profile = Profile.objects.filter(user=request.user.id).first()
    if profile is None:
        return HttpResponseRedirect(reverse("UserProfile:create_profile"))

    if request.method == "POST":
        form = RequestedBookForm(request.POST)
        if form.is_valid():
            request = form.save(commit=False)
            request.user = profile
            request.save()
            return HttpResponseRedirect(reverse("KatalogBuku:show_request_book"))
    else:
        form = RequestedBookForm()
    response = {
        "form": form,
    }
    return render(request, "form-request.html", response)
