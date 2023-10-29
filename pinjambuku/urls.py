from django.urls import path
from . import views

urlpatterns = [
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('return/<uuid:loan_id>/', views.return_book, name='return_book'),
    path('track_return_date/<uuid:loan_id>/', views.track_return_date, name='track_return_date'),
]