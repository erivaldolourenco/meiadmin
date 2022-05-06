from django.contrib import messages
from django.contrib.auth import logout as dash_logout, authenticate, login as dash_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from mei.forms import DespesaComprovadaForm
from mei.models import DespesaComprovada


def login(request):
    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['senha']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            dash_login(request, user)
            messages.add_message(
                request, messages.SUCCESS, 'Bem-vindo ' +
                str(user.first_name)+' '+str(user.last_name)+'!',
                fail_silently=True,
            )
            return redirect('/')
        else:
            messages.add_message(
                request, messages.ERROR, 'Usuário ou senha inválidos :(',
                fail_silently=True,
            )
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required
def logout(request):
    dash_logout(request)
    return redirect('/login')

@login_required
def home(request):
    template = loader.get_template('home.html')
    context = {'nfes': 'nfes'}
    return HttpResponse(template.render(context, request))

@login_required
def mei(request):
    template = loader.get_template('mei.html')
    context = {'nfes': 'nfes'}
    return HttpResponse(template.render(context, request))

@login_required
def despesas_comprovadas(request):
    despesas = DespesaComprovada.objects.all().filter(mei = request.user.responsavel.mei).order_by('-id')
    if request.method == 'POST':
        despesa = DespesaComprovada()
        despesa_form = DespesaComprovadaForm(request.POST, request.FILES, instance=despesa)
        if despesa_form.is_valid():
            despesa.mei = request.user.responsavel.mei
            despesa = despesa_form.save(commit=True)
            despesa.save()
            messages.add_message(
                request, messages.SUCCESS, 'Arquivo Adicionando com sucesso',
                fail_silently=True,
            )
            return redirect('/despesas')
        else:
            messages.add_message(
                request, messages.ERROR, 'Formulario contem erros',
                fail_silently=True,
            )
            data = {
                'medias': despesa,
                'media_form': despesa_form
            }
            return render(request, 'dashboard/library.html', data)

    else:
        despesa_form = DespesaComprovadaForm()
        template = loader.get_template('despesas_comprovadas.html')
        context = {
            'despesas': despesas,
            'despesa_form': despesa_form,
               }
    return HttpResponse(template.render(context, request))