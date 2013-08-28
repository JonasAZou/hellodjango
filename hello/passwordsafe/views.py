#-*- encoding: utf-8 -*-

from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import View
from django.utils import six

from pprint import pprint
import logging
from .forms import RegistryForm, LoginForm, PasswordForm
from .models import *

class PageRedirect(HttpResponse):
    def __init__(self, url, msg=None, timeout=3000):
        super(PageRedirect, self).__init__()

class MetaView(type):
    def __new__(cls, name, bases, attr):
        if not attr.get('template_name', None):
            attr['template_name'] = 'passwordsafe/{}.html'.format(name[:-4].lower())
        return super(MetaView, cls).__new__(cls, name, bases, attr)

class MyView(six.with_metaclass(MetaView)):
    require_auth = False
    def dispatch(self, request, *args, **kw):
        '''Subclasses should never override this'''
        if self.require_auth and not request.is_authenticated():
            pass
        try:
            method = getattr(self, request.method.lower())
            response = method(request, *args, **kw)
        except AttributeError:
            response = HttpResponseNotFound()
        if dict == type(response):
            return render(request, self.template_name, response)
        elif isinstance(response, HttpResponse):
            return response
        else:
            return HttpResponse('{}'.format(response))

    def get(self, request, *args, **kw):
        pass

    def post(self, request, *args, **kw):
        pass

    @classmethod
    def as_view(kls):
        return kls().dispatch

class IndexView(MyView):
    pass

@login_required(login_url='/passwordsafe/login/')
def index(request):
    pwds = Password.default_list(request.user)
    return render(request, 'passwordsafe/index.html', {
        'passwords': pwds
    })

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

@login_required(login_url='/passwordsafe/login/')
def add(request):
    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            data = form.cleaned_data
            data['user'] = request.user
            pwd = Password.new(**data)
            pwd.save()
            return page_redirect(request, '/passwordsafe/add/', u'添加成功')
    else:
        form = PasswordForm()
    return render(request, 'passwordsafe/add.html', {
        'form': form
    })

@login_required(login_url='/passwordsafe/login/')
def edit(request, password_id):
    pwd = get_object_or_404(Password, pk=password_id)
    if pwd.user.pk != request.user.pk:
        return HttpResponseNotFound()
    pwd.delete()
    return page_redirect(request, '/passwordsafe/')

@login_required(login_url='/passwordsafe/login/')
def delete(request, password_id):
    pwd = get_object_or_404(Password, pk=password_id)
    if pwd.user.pk != request.user.pk:
        return HttpResponseNotFound()
    pwd.delete()
    return page_redirect(request, '/passwordsafe/')

def page_redirect(request, url, msg=u'操作成功', timeout=3000):
    return render(request, 'passwordsafe/redirect.html', {
        'url': url, 
        'msg': msg,
        'timeout': timeout,
    })
