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
    escolha_notificacao = request.POST.getlist('escolha')
    agravo_notificacao = get_object_or_404(Agravo, nome=nome_agravo)
    notificacoes_mapa = Notificacao.objects.filter(agravo=agravo_notificacao)
    lista_notificacoes = get_list_or_404(Notificacao)
    flag_agravo = True
    agravos_mapa = []
    for i in lista_notificacoes:
        for j in agravos_mapa:
            if j == i.agravo:
                flag_agravo = False
        if flag_agravo:
            agravos_mapa.append(i.agravo)
        flag_agravo = True
    context = {
        'notificacoes_mapa': notificacoes_mapa,
        'agravos_mapa': agravos_mapa,
        'escolha_notificacao': escolha_notificacao,
        'google_api_key': GOOGLE_API_KEY
    }
    return render(request, 'site_mapa/mapa.html', context)
