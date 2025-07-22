from django.shortcuts import render, redirect, get_object_or_404
from .forms import LaptopForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Laptop, Contact
from django.db.models import Q
from django.contrib import messages


# Create your views here.
def search_laptops(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Laptop.objects.filter(
            Q(brand__icontains=query) |
            Q(cpu__icontains=query) |
            Q(gpu__icontains=query)
        )

    return render(request, 'asosiy.html', {
        'results': results,
        'query': query
    })





@login_required(login_url='get-login')
def create_laptop(request):
    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES)
        if form.is_valid():
            laptop = form.save(commit=False)
            laptop.author = request.user
            laptop.save()
            messages.success(request, "Noutbuk muvaffaqiyatli qo‘shildi!")
            return redirect('get-asosiy')
    else:
        form = LaptopForm()
    return render(request, 'laptop.html', {'form': form})




def laptop_update(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    if laptop.author != request.user:
        return redirect('laptop_detail', pk=pk)

    if request.method == 'POST':
        form = LaptopForm(request.POST, request.FILES, instance=laptop)
        if form.is_valid():
            form.save()
            return redirect('laptop_detail', pk=pk)
    else:
        form = LaptopForm(instance=laptop)

    return render(request, 'laptop.html', {'form': form})

@login_required(login_url='get-login')
def laptop_delete(request, pk):
    laptop = get_object_or_404(Laptop, pk=pk)
    if laptop.author == request.user:
        laptop.delete()
    return redirect('get-ish-uchun')



def contact_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        message = request.POST.get('message')

        Contact.objects.create(username=username, email=email, message=message)


        messages.success(request, "✅ Xabaringiz adminlarga yuborildi!")
        return redirect('get-asosiy')
    return render(request, 'contact.html')