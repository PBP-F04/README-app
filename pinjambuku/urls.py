from django.urls import path
from . import views

app_name = 'pinjambuku'

urlpatterns = [
    path('borrow/<uuid:book_id>/', views.borrow_book, name='borrow_book'),
    path('return/<uuid:loan_id>/', views.return_book, name='return_book'),
    path('track_return_date/<uuid:loan_id>/', views.track_return_date, name='track_return_date'),
    # path('check_book_stock/<uuid:book_id>/', views.check_book_stock, name='check_book_stock'),
    # path('find_book/', views.find_book, name='find_book'),
]
