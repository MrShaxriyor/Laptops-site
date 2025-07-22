from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from post.models import Laptop, Comment
from .forms import CommentForm

# Create your views here.

def home_view(request):
    return render(request, 'home.html')


def get_about(request):
    return render(request, 'about.html')

@login_required(login_url='get-login')
def get_contact(request):
    return render(request, 'contact.html')

@login_required(login_url='get-login')
def get_ish_uchun(request):
    laptops = Laptop.objects.filter(category__name__iexact='ish uchun')
    return render(request, 'category/ish_uchun.html', {'laptops': laptops})

@login_required(login_url='get-login')
def get_gaming(request):
    laptops = Laptop.objects.filter(category__name__iexact='Gaming')
    return render(request, 'category/gaming.html', {'laptops': laptops})

@login_required(login_url='get-login')
def get_student(request):
    laptops = Laptop.objects.filter(category__name__iexact='Student')
    return render(request, 'category/students.html',{'laptops': laptops})

@login_required(login_url='get-login')
def get_premium(request):
    laptops = Laptop.objects.filter(category__name__iexact='Priemum')
    return render(request, 'category/pr_model.html',{'laptops': laptops})

@login_required(login_url='get-login')
def get_asosiy(request):
    return render(request, 'asosiy.html')

@login_required(login_url='get-login')
def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    return render(request, 'laptop_detail.html', {'laptop': laptop})


def laptop_detail(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    comments = laptop.comments.all().order_by('-created_at')
    form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.laptop = laptop
                comment.user = request.user
                comment.save()
                return redirect('laptop_detail', pk=pk)
        else:
            return redirect('get-login')

    return render(request, 'laptop_detail.html', {
        'laptop': laptop,
        'comments': comments,
        'form': form
    })