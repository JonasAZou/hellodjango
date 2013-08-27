#-*- encoding: utf-8 -*-

from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse
from pprint import pprint
import logging
import hello.settings
from .forms import RegistryForm, LoginForm

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

log = logging.getLogger('debug')

def index(request):
    log = logging.getLogger('debug')
    log.debug(__file__)
    user = getattr(request, 'user', None)
    io = StringIO()
    if user:
        pprint(user.is_authenticated(), io)
        io.write('\n date_joined={}, username={}, passwd={} \n'.format(user.date_joined, user.username, user.password))
    pprint(user, io)
    pprint(vars(hello.settings), io)
    return HttpResponse('<pre>' + io.getvalue() + '</pre>')

def register(request):
    if request.method == 'POST':
        form = RegistryForm(request.POST)
        if form.is_valid():
            loginname = form.cleaned_data['loginname']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(loginname, email, password)
            return HttpResponse('thank you, ok!')
    else:
        form = RegistryForm()
    return render(request, 'passwordsafe/registry.html', {
        'form': form,
    })

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_user(request, form.cleaned_data['user'])
            return HttpResponse('welcome {}'.format(form.cleaned_data['user'].username))
    else:
        form = LoginForm()
    return render(request, 'passwordsafe/login.html', {
        'form': form,
    })

def logout(request):
    if request.user.is_authenticated():
        msg = 'goodbye, {}'.format(request.user.username)
        log.debug(request.user)
    else:
        msg = 'you are not logged in!'
    logout_user(request)
    return HttpResponse(msg)
