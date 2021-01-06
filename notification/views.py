from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers
from .forms import *
import json
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
def notificacao_list(request):
    # IF responsável por modificar o campo situação atual
    if request.method == 'POST':
        notificacao = get_object_or_404(Notificacao, id=request.POST['notificacao_valor'])
        notificacao.situacao_atual = request.POST['situacao_notificacao']
        notificacao.save()
        notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('agravo')
        lista_notificacoes = []
        for notificacao in notificacoes:
            aux = {
                "id":notificacao.id,
                "paciente":notificacao.paciente.nome,
                "agravo":notificacao.agravo.nome,
                "unidade_saude":notificacao.unidade_saude.nome,
                "situacao_atual":notificacao.situacao_atual,
            }
            lista_notificacoes.append(aux)
        return JsonResponse(lista_notificacoes, safe=False, status=200)
    else:
        notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('agravo')
        agravos_mapa = Agravo.objects.all()
        if (notificacoes):
            lista_notificacoes = []
            for notificacao in notificacoes:
                aux = {
                    "id":notificacao.id,
                    "paciente":notificacao.paciente.nome,
                    "agravo":notificacao.agravo.nome,
                    "unidade_saude":notificacao.unidade_saude.nome,
                    "situacao_atual":notificacao.situacao_atual,
                }
                lista_notificacoes.append(aux)
            context = {
                'notificacoes': lista_notificacoes,
                'agravos_mapa': agravos_mapa
            }
        else:
            context = {'agravos_mapa': agravos_mapa}
        return render(request, "notification/notificacao_list.html", context)

@login_required
def novo_notificacao(request):
    if request.method == 'POST':
        notificacao_form = NotificacaoForm(request.POST)
        if notificacao_form.is_valid():
            if(request.session.get('paciente_cns')):
                notificacao = notificacao_form.save(commit=False)
                paciente_notificacao = get_object_or_404(Paciente, cns=request.session.get('paciente_cns'))
                user = request.user
                notificacao.usuario = user
                notificacao.paciente = paciente_notificacao
                notificacao.save()
                notificacao_form.save_m2m()
                del request.session['paciente_cns']
                messages.success(
                    request, f'{user.nome}, notificação realizada com sucesso!')
                return redirect('notification:notificacao_list')
            else:
                notificacao = notificacao_form.save(commit=False)
                user = request.user
                notificacao.usuario = user
                notificacao.save()
                notificacao_form.save_m2m()
                messages.success(
                    request, f'{user.nome}, notificação realizada com sucesso!')
                return redirect('notification:notificacao_list')
    else:
        notificacao_form = NotificacaoForm()  
    lista_ubs = Estabelecimento.objects.all()
    agravos_mapa = Agravo.objects.all()
    if(request.session.get('paciente_cns')):
        context = {
            'notificacao_form': notificacao_form,
            'paciente_cns': get_object_or_404(Paciente, cns=request.session.get('paciente_cns')),
            'lista_ubs': lista_ubs,
            'agravos_mapa': agravos_mapa,
        }
    else:
        context = {
            'notificacao_form': notificacao_form,
            'lista_ubs': lista_ubs,
            'agravos_mapa': agravos_mapa,
        }
    return render(request, 'notification/novo_notificacao.html', context)

@login_required
def descobre_agravo(request):
    agravo = get_object_or_404(Agravo, id=request.POST['id_agravo'])
    sinais_clinicos = agravo.sinais_clinicos.all().values()
    doencas_pre_existentes = agravo.doencas_pre_existentes.all().values()
    return JsonResponse({'sinais_clinicos':list(sinais_clinicos), 'doencas_pre_existentes':list(doencas_pre_existentes)}, status=200)