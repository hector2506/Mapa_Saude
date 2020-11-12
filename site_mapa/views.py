from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .forms import *
from notification.models import *
import os

@login_required
def mapa(request):
    env = os.environ
    GOOGLE_API_KEY = env.get('GOOGLE_API_KEY')
    nome_agravo = request.POST['agravo_notificacao']
    agravo_notificacao = Agravo.objects.get(nome=nome_agravo)
    notificacoes_mapa = Notificacao.objects.filter(agravo=agravo_notificacao)
    lista_notificacoes = Notificacao.objects.all()
    ubs_mapa = get_list_or_404(Estabelecimento)
    flag_agravo = True
    agravos_mapa = Agravo.objects.all()
    context = {
        'nome_agravo': nome_agravo,
        'notificacoes_mapa': notificacoes_mapa,
        'ubs_mapa': ubs_mapa,
        'agravos_mapa': agravos_mapa,
        'google_api_key': GOOGLE_API_KEY
    }
    return render(request, 'site_mapa/mapa.html', context)
