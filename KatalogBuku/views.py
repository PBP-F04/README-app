from django.shortcuts import render
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import Book, Category, BookLike, RequestedBook
import datetime
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from UserProfile.models import Profile
from django.views.decorators.csrf import csrf_exempt


@require_http_methods(['GET'])
def index(request):
    user = request.user
    response = {
        "user": user
    }
    return render(request, 'katalog.html', response)


@require_http_methods(['GET'])
def get_books(request):
    category = request.GET.get('category', None)
    sort = request.GET.get('sort', None)
    order = request.GET.get('order', None)
    page = request.GET.get('page', 1)
    search = request.GET.get('search', None)
    items_per_page = 20

    allowed_sort = ['issued', 'title', 'author', 'subject', 'category']

    if order is not None and (order != 'asc' and order != 'desc'):
        order = None

    if sort is not None and sort not in allowed_sort:
        sort = None

    if sort is None and category is None and order is None and search is None:
        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').order_by('book_code').all()
                 )
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is None and category is None and order is None and search is not None:
        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').filter(title__contains=search).order_by('book_code').all()
                 )
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is None and category is None and order is not None and search is None:
        if order == 'asc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by('book_code').all()
                     )
        elif order == 'desc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by('-book_code').all()
                     )
        else:
            response = {
                'status': 400,
                'message': 'Bad Request',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is None and category is None and order is not None and search is not None:
        if order == 'asc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').filter(title__contains=search).order_by('book_code').all()
                     )
        elif order == 'desc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').filter(title__contains=search).order_by('-book_code').all()
                     )
        else:
            response = {
                'status': 400,
                'message': 'Bad Request',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is None and category is not None and order is None and search is None:
        list_category = category.split(';')
        selected_category = Category.objects.filter(category_name__in=list_category).all()
        selected_category = list(selected_category)
        if len(selected_category) == 0:
            response = {
                'status': 400,
                'message': 'Category not found',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').order_by('book_code').filter(category__in=selected_category)
                 )
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is None and category is not None and order is None and search is not None:
        list_category = category.split(';')
        selected_category = Category.objects.filter(category_name__in=list_category).all()
        selected_category = list(selected_category)
        if len(selected_category) == 0:
            response = {
                'status': 400,
                'message': 'Category not found',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').order_by('book_code').filter(category__in=selected_category).filter(
            title__contains=search)
        )
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is None and order is None and search is None:
        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').order_by(sort).all()
                 )
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is None and order is None and search is not None:
        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').filter(title__contains=search).order_by(sort).all()
                 )
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is None and order is not None and search is None:
        if order == 'asc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by(sort).all()
                     )
        elif order == 'desc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by('-' + sort).all()
                     )
        else:
            response = {
                'status': 400,
                'message': 'Bad Request',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        books = return_book(books)
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is None and order is not None and search is not None:
        if order == 'asc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').filter(title__contains=search).order_by(sort).all()
                     )
        elif order == 'desc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').filter(title__contains=search).order_by('-' + sort).all()
                     )
        else:
            response = {
                'status': 400,
                'message': 'Bad Request',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is not None and order is None and search is None:
        list_category = category.split(';')
        selected_category = Category.objects.filter(category_name__in=list_category).all()
        selected_category = list(selected_category)
        if len(selected_category) == 0:
            response = {
                'status': 400,
                'message': 'Category not found',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').order_by(sort).filter(category__in=selected_category)
                 )

        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is not None and order is None and search is not None:
        list_category = category.split(';')
        selected_category = Category.objects.filter(category_name__in=list_category).all()
        selected_category = list(selected_category)
        if len(selected_category) == 0:
            response = {
                'status': 400,
                'message': 'Category not found',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        books = (Book.objects.select_related('Category').values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').order_by(sort).filter(category__in=selected_category).filter(
            title__contains=search)
        )

        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is not None and order is not None and search is None:
        list_category = category.split(';')
        selected_category = Category.objects.filter(category_name__in=list_category).all()
        selected_category = list(selected_category)
        if len(selected_category) == 0:
            response = {
                'status': 400,
                'message': 'Category not found',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        if order == 'asc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by(sort).filter(category__in=selected_category)
                     )
        elif order == 'desc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by('-' + sort).filter(category__in=selected_category)
                     )
        else:
            response = {
                'status': 400,
                'message': 'Bad Request',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)

    if sort is not None and category is not None and order is not None and search is not None:
        list_category = category.split(';')
        selected_category = Category.objects.filter(category_name__in=list_category).all()
        selected_category = list(selected_category)
        if len(selected_category) == 0:
            response = {
                'status': 400,
                'message': 'Category not found',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)

        if order == 'asc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by(sort).filter(category__in=selected_category).filter(
                title__contains=search)
            )
        elif order == 'desc':
            books = (Book.objects.select_related('Category').values(
                'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
                'category__category_name').order_by('-' + sort).filter(category__in=selected_category).filter(
                title__contains=search)
            )
        else:
            response = {
                'status': 400,
                'message': 'Bad Request',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=400)
        paginator = Paginator(books, items_per_page)
        try:
            books_pages = paginator.page(page)
        except PageNotAnInteger:
            books_pages = paginator.page(1)
        except EmptyPage:
            books_pages = paginator.page(paginator.num_pages)
        books = return_book(books_pages)
        response = {
            'status': 200,
            'message': 'success',
            'data': books,
            'pagination': {
                'current_page': books_pages.number,
                'total_page': books_pages.paginator.num_pages,
                'has_previous': books_pages.has_previous(),
                'has_next': books_pages.has_next(),
            }
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)


@require_http_methods(['GET'])
@login_required(login_url='authentication:login')
def get_categories(request):
    categories = Category.objects.values('id', 'category_name').all()
    categories = list(categories)
    for category in categories:
        category['id'] = str(category['id'])

    response = {
        'status': 200,
        'message': 'success',
        'data': categories
    }
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)


@require_http_methods(['GET'])
@login_required(login_url='authentication:login')
def get_book_by_id(request, book_id):
    try:
        user = request.user
        profile = Profile.objects.filter(user=user.id).first()
        if profile is None:
            return HttpResponseRedirect(reverse('UserProfile:create_profile'))
        book = Book.objects.filter(id=book_id).values(
            'id', 'issued', 'book_code', 'title', 'author', 'book_read_url', 'subject', 'synopsis',
            'category__category_name').first()
        if book is None:
            response = {
                'status': 404,
                'message': 'Book not found',
            }
            return HttpResponse(json.dumps(response), content_type='application/json', status=404)
        book_like = BookLike.objects.filter(book=book['id'], user=profile).first()
        if book_like is None:
            book['is_liked'] = False
        else:
            book['is_liked'] = True

        book['id'] = str(book['id'])
        book['category'] = book['category__category_name']
        issued = book['issued'].split('-')
        issued = datetime.date(int(issued[0]), int(issued[1]), int(issued[2]))
        book['issued'] = issued.strftime("%d %B %Y")
        del book['category__category_name']
        response = {
            'status': 200,
            'message': 'success',
            'data': book
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)
    except ValidationError as e:
        response = {
            'status': 400,
            'message': 'Bad Request',
        }
        return HttpResponseRedirect(reverse('KatalogBuku:index'))


@require_http_methods(['POST'])
@login_required()
@csrf_exempt
def like_book(request, book_id):
    user = request.user
    book = Book.objects.filter(id=book_id).first()
    profile = Profile.objects.filter(user=user.id).first()
    if book is None:
        response = {
            'status': 404,
            'message': 'Book not found',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=404)
    book_like = BookLike.objects.filter(book=book, user=profile).first()
    if book_like is None:
        BookLike.objects.create(book=book, user=profile)
        response = {
            'status': 200,
            'message': 'success',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)
    else:
        response = {
            'status': 400,
            'message': 'Book already liked',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)


@csrf_exempt
def unlike_book(request, book_id):
    user = request.user
    book = Book.objects.filter(id=book_id).first()
    profile = Profile.objects.filter(user=user.id).first()
    if book is None:
        response = {
            'status': 404,
            'message': 'Book not found',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=404)
    book_like = BookLike.objects.filter(book=book, user=profile).first()
    if book_like is None:
        response = {
            'status': 400,
            'message': 'Book not liked',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)
    else:
        book_like.delete()
        response = {
            'status': 200,
            'message': 'success',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)


@require_http_methods(['GET'])
@login_required(login_url='authentication:login')
def show_request_book(request):
    return render(request, 'request_book.html')


@require_http_methods(['POST'])
@login_required(login_url='authentication:login')
@csrf_exempt
def create_request_book(request):
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError as e:
        response = {
            'status': 400,
            'message': 'Bad Request',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)
    title = body['title']
    author = body['author']
    book_url = body['book_url']
    reason = body['reason']
    user = request.user
    user_profile = Profile.objects.filter(user=user.id).first()

    if RequestedBook.objects.filter(title=title).exists():
        response = {
            'status': 400,
            'message': 'Book already requested',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)

    if title is None or author is None or book_url is None or reason is None:
        response = {
            'status': 400,
            'message': 'Bad Request',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)
    try:
        RequestedBook.objects.create(title=title, author=author, book_url=book_url, reason=reason, user=user_profile)
        response = {
            'status': 200,
            'message': 'success',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=200)
    except ValidationError as e:
        response = {
            'status': 400,
            'message': 'Bad Request',
        }
        return HttpResponse(json.dumps(response), content_type='application/json', status=400)


@require_http_methods(['GET'])
@login_required(login_url='authentication:login')
@csrf_exempt
def get_requested_book(request):
    page = request.GET.get('page', 1)
    items_per_page = 20
    requested_books = RequestedBook.objects.values('id', 'title', 'author', 'book_url', 'reason',
                                                   'user__username').all()
    requested_books = list(requested_books)
    paginator = Paginator(requested_books, items_per_page)
    try:
        requested_books_pages = paginator.page(page)
    except PageNotAnInteger:
        requested_books_pages = paginator.page(1)
    except EmptyPage:
        requested_books_pages = paginator.page(paginator.num_pages)

    for requested_book in requested_books_pages.object_list:
        requested_book['id'] = str(requested_book['id'])
        requested_book['user'] = requested_book['user__username']
        del requested_book['user__username']
    response = {
        'status': 200,
        'message': 'success',
        'data': requested_books_pages.object_list,
        'pagination': {
            'current_page': requested_books_pages.number,
            'total_page': requested_books_pages.paginator.num_pages,
            'has_previous': requested_books_pages.has_previous(),
            'has_next': requested_books_pages.has_next(),
        }
    }
    return HttpResponse(json.dumps(response), content_type='application/json', status=200)


def return_book(books):
    books = books.object_list
    books = list(books)
    for book in books:
        book['category'] = book['category__category_name']
        del book['category__category_name']
        book['id'] = str(book['id'])
        issued = book['issued'].split('-')
        issued = datetime.date(int(issued[0]), int(issued[1]), int(issued[2]))
        book['issued'] = issued.strftime("%d %B %Y")
    return books
