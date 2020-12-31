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
    pacientes = Paciente.objects.filter(ubs=request.user.vinculo).order_by('nome')
    agravos_mapa = Agravo.objects.all()
    if (pacientes):
        context = {
            'pacientes': pacientes,
            'agravos_mapa': agravos_mapa
        }
    else:
        context = {'agravos_mapa': agravos_mapa}
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
    ubs_mapa = Estabelecimento.objects.all()
    agravos_mapa = Agravo.objects.all()
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')
    context = {
        'ubs_mapa': ubs_mapa,
        'agravos_mapa': agravos_mapa,
        'google_api_key': GOOGLE_API_KEY,
        'form': form,
    }
    return render(request, 'patient/novo_paciente.html', context)
