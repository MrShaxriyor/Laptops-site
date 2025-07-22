from django.urls import path
from .views import *

urlpatterns = [
    path('', home_view, name='get-home'),
    path('about/', get_about, name='get-about'),
    path('call/', get_contact, name='get-contact'),
    path('ish_uchun/', get_ish_uchun, name='get-ish-uchun'),
    path('gaming/', get_gaming, name='get-gaming'),
    path('student/', get_student, name='get-student'),
    path('premium/', get_premium, name='get-premium'),
    path('asosiy/', get_asosiy, name='get-asosiy'),
    path('laptop/<int:pk>/', laptop_detail, name='laptop_detail'),
]