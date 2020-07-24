from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .forms import *
import os

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        cpf = form.cleaned_data.get('cpf')
        password = form.cleaned_data.get('password')
        user = authenticate(username=cpf,password=password)
        login(request, user)
        return redirect('patient:home')
    context = {
        'form': form
    }
    return render(request,'accounts/login.html',context)


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password1')
            user.set_password(password)
            user.save()
            messages.success(
                request, f'{user.nome}, conta criada com sucesso!')
            new_user = authenticate(username=user.cpf, password=password)
            login(request, new_user)
            return redirect('patient:home')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/cadastrar_usuario.html', context)


def logout_view(request):
    logout(request)
    return redirect('accounts:login')