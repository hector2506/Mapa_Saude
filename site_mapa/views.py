from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .forms import *
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


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        cpf = form.cleaned_data.get('cpf')
        password = form.cleaned_data.get('password')
        user = authenticate(username=cpf,password=password)
        login(request, user)
        return redirect('home')
    context = {
        'form': form
    }
    return render(request,'login.html',context)


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
            return redirect('home')
    else:
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'cadastrar_usuario.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def notificacao_list(request):
    # IF responsável por modificar o campo situação atual
    if request.method == 'POST':
        notificacao = get_object_or_404(Notificacao, id=request.POST['notificacao_valor'])
        notificacao.situacao_atual = request.POST['situacao_notificacao']
        notificacao.save()
    notificacoes = gerenciar_paginacao(request, Notificacao.objects.filter(usuario=request.user))
    lista_notificacoes = Notificacao.objects.all()
    if (notificacoes):
        agravos_mapa = []
        if(lista_notificacoes):
            flag_agravo = True
            for i in lista_notificacoes:
                for j in agravos_mapa:
                    if j == i.agravo:
                        flag_agravo = False
                if flag_agravo:
                    agravos_mapa.append(i.agravo)
                flag_agravo = True
        context = {
            'notificacoes': notificacoes,
            'agravos_mapa': agravos_mapa
        }
    else:
        context = {}
    return render(request, "notificacao_list.html", context)


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
    return render(request, "home.html", context)


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
            return redirect('novo_notificacao')
    else:
        form = PacienteRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'novo_paciente.html', context)


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
                del request.session['paciente_cns']
                messages.success(
                    request, f'{user.nome}, notificação realizada com sucesso!')
                return redirect('notificacao_list')
            else:
                notificacao = notificacao_form.save(commit=False)
                user = request.user
                notificacao.usuario = user
                notificacao.save()
                messages.success(
                    request, f'{user.nome}, notificação realizada com sucesso!')
                return redirect('notificacao_list')
    else:
        notificacao_form = NotificacaoForm()
    if(request.session.get('paciente_cns')):
        context = {
            'notificacao_form': notificacao_form,
            'paciente_cns': get_object_or_404(Paciente, cns=request.session.get('paciente_cns'))
        }
    else:
        context = {
            'notificacao_form': notificacao_form,
        }
    return render(request, 'novo_notificacao.html', context)


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
    return render(request, 'mapa.html', context)
