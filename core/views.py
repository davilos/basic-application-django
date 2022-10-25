from django.shortcuts import render
from .forms import ContatoForm, ProdutoModelForm
from django.contrib import messages
from .models import Produto
from django.shortcuts import redirect
# from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def index(request):
    context = {'produtos': Produto.objects.all()}
    return render(request, 'index.html', context)


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
    print(request)
    if request.user.is_authenticated:
        return redirect('index', messages.warning(request, 'Você já está cadastrado!'))
    try:
        user_aux = User.objects.get(email=request.POST['email'])

        if user_aux:
            return render(request, 'cadastro.html', messages.error(request, 'Já existe um usuário com este e-mail!'))
    except User.DoesNotExist:
        if (request.POST['password'] == request.POST['password-conf']):
            user = User.objects.create_user(request.POST['user'], request.POST['email'], request.POST['password'])
            user.save()
            
            return render(request, 'cadastro.html', messages.success(request, f'Seja bem-vindo {user.username}!'))
        else:
            return render(request, 'cadastro.html', messages.error(request, 'As senha não são iguais!'))


def logar(request):
    if request.user.is_authenticated:
        return redirect('index', messages.warning(request, 'Você já está logado!'))
    user_aux = User.objects.get(email=request.POST['email'])
    user = authenticate(username=user_aux.username, password=request.POST['password'])

    if user is not None:
        login(request, user)
        return redirect('index', messages.success(request, f'Bem-vindo novamente, {str(user.username)}'))
    else:
         return render(request, 'login.html', messages.error(request, 'Usuário ou senha incorretos!'))


@login_required
def sair(request):
    logout(request)
    return redirect('index')
