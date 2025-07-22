from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
import random
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import make_password


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords notugri")
            return redirect('get-sign')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username mavjud")
            return redirect('get-sign')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Successfully")
        return redirect('get-login')

    return render(request, 'account/reg.html')



def get_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Email topilmadi.')
            return redirect('get-login')

        user = authenticate(request, username=user_obj.username, password=password)
        if user is not None:
            login(request, user)
            return redirect('get-asosiy')
        else:
            messages.error(request, 'Parol noto‘g‘ri.')
            return redirect('get-login')

    return render(request, 'account/login.html')


def get_log(request):
    logout(request)
    return redirect('get-home')

def ykod(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        code = str(random.randint(100000, 999999))
        request.session['verify_code'] = code
        request.session['verify_email'] = email

        send_mail(
            'Profil yangilash uchun tasdiqlash kodi',
            f'Sizning tasdiqlash kodingiz: {code}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
        return redirect('tekshir')
    return render(request, 'account/ykod.html')

def verify_code(request):
    if request.method == 'POST':
        input_code = request.POST.get('code')
        session_code = request.session.get('verify_code')
        if input_code == session_code:
            return redirect('update-profile')
        else:
            return render(request, 'account/tekshir.html', {'error': 'Kod noto‘g‘ri'})
    return render(request, 'account/tekshir.html')


@login_required(login_url='get-login')
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password == confirm:
            user.username = username
            user.set_password(password)
            user.save()
            update_session_auth_hash(request, user)  # login holatini saqlab qoladi
            return redirect('get-asosiy')
        else:
            return render(request, 'account/update.html', {'error': 'Parollar mos emas'})

    return render(request, 'account/update.html', {'user': user})




def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            code = random.randint(100000, 999999)
            request.session['reset_email'] = email
            request.session['reset_code'] = str(code)

            send_mail(
                subject='🔐 Parolni tiklash kodi',
                message=f"Sizning parol tiklash kodingiz: {code}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            return redirect('verify-code')
        else:
            return render(request, 'account/forgot_password.html', {'error': 'Bunday email topilmadi'})
    
    return render(request, 'account/forgot_password.html')


def verify_code(request):
    if request.method == 'POST':
        input_code = request.POST.get('code')
        session_code = request.session.get('reset_code')

        if input_code == session_code:
            return redirect('set-new-password')
        else:
            return render(request, 'account/verify_code.html', {'error': 'Kod noto‘g‘ri'})

    return render(request, 'account/verify_code.html')


def set_new_password(request):
    if request.method == 'POST':
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'account/set_new_password.html', {'error': 'Parollar mos emas'})

        email = request.session.get('reset_email')
        if not email:
            return redirect('forgot-password')

        user = User.objects.filter(email=email).first()
        if user:
            user.password = make_password(password1)
            user.save()
            request.session.flush()
            return redirect('get-login')

    return render(request, 'account/set_new_password.html')