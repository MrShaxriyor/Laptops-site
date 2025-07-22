from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', signup, name='get-sign'),
    path('login/', get_login, name='get-login'),
    path('log/', get_log, name='get-log'),
    path('profile/verify-email/', ykod, name='get-code'),
    path('profile/verify-code/', verify_code, name='tekshir'),
    path('profile/update/', update_profile, name='update-profile'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('verify-code/', verify_code, name='verify-code'),
    path('set-new-password/', set_new_password, name='set-new-password'),


]