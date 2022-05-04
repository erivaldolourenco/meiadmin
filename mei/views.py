from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader


def login(request):
    template = loader.get_template('login.html')
    context = {'nfes': 'nfes'}
    return HttpResponse(template.render(context, request))
@login_required
def home(request):
    template = loader.get_template('home.html')
    context = {'nfes': 'nfes'}
    return HttpResponse(template.render(context, request))