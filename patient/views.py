from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .forms import *
from notification.models import *
import os

def gerenciar_paginacao(request, object_list):
    paginator = Paginator(object_list, 5)
    try:
        page_num = int(request.GET.get('page', '1'))
        if page_num < 1:
            page_num = 1
    except ValueError:
        page_num = 1
    try:
        current_page = paginator.page(page_num)
    except (InvalidPage, EmptyPage):
        current_page = paginator.page(paginator.num_pages)
    return current_page

@login_required
def paciente_list(request):
    pacientes = gerenciar_paginacao(request, Paciente.objects.filter(ubs=request.user.vinculo))
    lista_notificacoes = Notificacao.objects.all()
    if (pacientes):
        agravos_mapa = []
        if (lista_notificacoes):
            flag_agravo = True
            for i in lista_notificacoes:
                for j in agravos_mapa:
                    if j == i.agravo:
                        flag_agravo = False
                if flag_agravo:
                    agravos_mapa.append(i.agravo)
                flag_agravo = True
        context = {
            'pacientes': pacientes,
            'agravos_mapa': agravos_mapa
        }
    else:
        context = {}
    return render(request, "patient/home.html", context)

@login_required
def novo_paciente(request):
    if request.method == 'POST':
        form = PacienteRegisterForm(request.POST)
        if form.is_valid():
            paciente = form.save(commit=False)
            user = request.user
            paciente.ubs = user.vinculo
            paciente.save()
            request.session['paciente_cns'] = paciente.cns
            messages.success(
                request, f'Paciente {paciente.nome} registrado com sucesso! Prosseguindo com a notificação:')
            return redirect('notification:novo_notificacao')
    else:
        form = PacienteRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'patient/novo_paciente.html', context)