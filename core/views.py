from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import ContatoForm, ProdutoModelForm
from .models import Produto


def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    context = {'produtos': Produto.objects.all()}
    return render(request, 'index.html', context)


def index_on(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/')
    context = {
        'produtos': Produto.objects.all(),
        'msg': f'Bem-vindo, {str(request.user.username)}!',
        'class': 'alert-dark',
    }
    return render(request, 'indexon.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            form.send_email()

            messages.success(request, 'E-mail enviado com sucesso!')

            form = ContatoForm()
        else:
            messages.error(request, 'Erro ao enviar e-mail!')

    context = {'form': form}
    return render(request, 'contato.html', context)


def produto(request):
    if request.user.is_staff:
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()

                messages.success(request, 'Produto salvo com sucesso!')

                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar produto.')
        else:
            form = ProdutoModelForm()
        context = {'form': form}
        return render(request, 'produto.html', context)
    else:
        return redirect('index')


def cadastro(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    return render(request, 'cadastro.html')


@require_POST
def cadastro_conf(request):
    context = {}
    confirm = [
        request.POST['user']
        + request.POST['email']
        + request.POST['password']
        + request.POST['password-conf']
    ]

    if confirm[0] == '':
        context['msg'] = 'Insira todos os dados!'
        context['class'] = 'alert-danger'
        return render(request, 'cadastro.html', context)

    try:
        user_aux = User.objects.get(email=request.POST['email'])

        if user_aux:
            context['msg'] = 'Já existe um usuário com este e-mail!'
            context['class'] = 'alert-warning'
    except User.DoesNotExist:
        try:
            if request.POST['password'] != request.POST['password-conf']:
                context['msg'] = 'As senha não são iguais!'
                context['class'] = 'alert-danger'
            elif (
                str(request.POST['password']) == ''
                and str(request.POST['password-conf']) == ''
            ):
                context['msg'] = 'Insira as senhas corretamente!'
                context['class'] = 'alert-danger'
            elif len(str(request.POST['email'])) == 0:
                context['msg'] = 'Insira um e-mail!'
                context['class'] = 'alert-danger'
            elif (
                len(str(request.POST['password'])) < 8
                and len(str(request.POST['password-conf'])) < 8
            ):
                context[
                    'msg'
                ] = 'Insira uma senha maior ou igual a 8 caracteres'
                context['class'] = 'alert-warning'
            else:
                user = User.objects.create_user(
                    request.POST['user'],
                    request.POST['email'],
                    request.POST['password'],
                )
                user.save()
                login(request, user)
                return HttpResponseRedirect('/home/')
        except ValueError:
            context['msg'] = 'Insira um nome de usuário correto!'
            context['class'] = 'alert-danger'
    return render(request, 'cadastro.html', context)


def logar(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/home/')
    return render(request, 'login.html')


@require_POST
def logar_conf(request):
    context = {}
    confirm = [request.POST['email'] + request.POST['password']]

    if confirm[0] == '':
        context['msg'] = 'Insira todos os dados!'
        context['class'] = 'alert-danger'
    elif str(request.POST['password']) == '':
        context['msg'] = 'Insira uma senha!'
        context['class'] = 'alert-danger'
    elif str(request.POST['email']) == '':
        context['msg'] = 'Insira um e-mail!'
        context['class'] = 'alert-danger'
    else:
        try:
            user_aux = User.objects.get(email=request.POST['email'])
            user = authenticate(
                username=user_aux.username, password=request.POST['password']
            )

            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                context['msg'] = 'E-mail ou senha incorretos!'
                context['class'] = 'alert-danger'

        except User.DoesNotExist:
            context['msg'] = 'Usuário não existe!'
            context['class'] = 'alert-danger'
    return render(request, 'login.html', context)


@login_required
def sair(request):
    logout(request)
    return redirect('index')
