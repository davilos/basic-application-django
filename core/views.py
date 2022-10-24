from django.shortcuts import render
from .forms import ContatoForm, ProdutoModelForm, CadastroModelForm
from django.contrib import messages
from .models import Produto
from django.shortcuts import redirect


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
    if str(request.method) == 'POST':
        form = CadastroModelForm(request.POST)

        if form.is_valid():
            print(form)

            messages.success(request, 'Cadastro realizado!')

            form = CadastroModelForm()
        else:
            messages.error(request, 'Erro ao relizar o cadastro.')
    else:
        form = CadastroModelForm()
    
    context = {'form': form}
    return render(request, 'cadastro.html', context)
