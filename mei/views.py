from django.contrib import messages
from django.contrib.auth import logout as dash_logout, authenticate, login as dash_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader


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