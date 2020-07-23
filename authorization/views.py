from django.shortcuts import render,redirect
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def login_page(request):
    """Рендер сторінки входу"""
    if request.user.is_authenticated:
        return redirect('http://127.0.0.1:8000/authorization')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("http://127.0.0.1:8000/")
            else:
                messages.info(request, 'Username or passwords is incorrect!')
        context = {}
        return render(request, 'login.html', context)


def register(request):
    """Рендер сторінки реєстрації"""
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'account.html', context)


def logout_user(request):
    """Рендер сторінки виходу"""
    logout(request)
    return redirect('register')
