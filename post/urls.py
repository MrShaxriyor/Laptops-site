from django.urls import path
from .views import *

urlpatterns = [
    path('create-laptop/', create_laptop, name='create-lap'),
    path('laptop-update/<int:pk>/', laptop_update, name='laptop_update'),
    path('laptop-delete/<int:pk>/', laptop_delete, name='laptop_delete'),
    path('search/', search_laptops, name='search_laptops'),
    path('contact/', contact_view, name='contact'),

]