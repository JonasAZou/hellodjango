# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
import hello.settings
from .forms import RegistryForm

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

def index(request):
    user = getattr(request, 'user', None)
    io = StringIO()
    if user:
        pprint(user.is_authenticated(), io)
        io.write('\n date_joined={}, username={}, passwd={} \n'.format(user.date_joined, user.username, user.password))
    pprint(user, io)
    pprint(vars(hello.settings), io)
    return HttpResponse(io.getvalue())

def register(request):
    if request.method == 'POST':
        form = RegistryForm(request.POST)
        loginname = form.cleaned_data['loginname']
        password = form.cleaned_data['password']
        repasswd = form.cleaned_data['repasswd']
        email = form.cleaned_data['email']
        if form.is_valid():
            return HttpResponse('thank you, ok!')
    else:
        form = RegistryForm()
    return render(request, 'passwordsafe/registry.html', {
        'form': form,
    })

def login(request):
    pass

def logout(request):
    pass
