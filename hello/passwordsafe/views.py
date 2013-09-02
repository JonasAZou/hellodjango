#-*- encoding: utf-8 -*-

from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic.base import View, TemplateView
from django.utils.http import urlquote_plus
from django.template import RequestContext, loader

import json

from pprint import pprint
import logging
from .forms import RegistryForm, LoginForm, PasswordForm
from .models import *

class JsonResponse(HttpResponse):
    def __init__(self, data=None, errno=0, errmsg='', *args, **kwargs):
        super(JsonResponse, self).__init__(*args, **kwargs)
        if errno or errmsg:
            ret = {
                'errno': errno,
                'errmsg': errmsg,
            }
        else:
            ret = {
                'data': data
            }
        self.write( json.dumps(ret) )

class MyView(View):
    require_auth = False

    def page_redirect(self, url, msg=None, timeout=3000):
        return render(self.request, 'passwordsafe/redirect.html', {
            'url': url,
            'msg': msg,
            'timeout': timeout,
        })

    def __init__(self, *args, **kwargs):
        if not getattr(self, 'template_name', None):
            self.template_name = 'passwordsafe/{}.html'.format(self.__class__.__name__[:-4].lower())
        super(MyView, self).__init__(*args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if self.require_auth and not self.request.user.is_authenticated():
            return self.page_redirect(
                '{}?next={}'.format(reverse('passwordsafe:login'),urlquote_plus(request.path)),
                u'请先登录')
        return super(MyView, self).dispatch(request, *args, **kwargs)

class IndexView(MyView):

    def get(self, request, *args, **kwargs):
        # pwds = Password.default_list(request.user)
        return render(request, self.template_name, {
            #'passwords': pwds
        })

class RegisterView(MyView):
    def get(self, request, *args, **kwargs):
        form = RegistryForm()
        return render(request, 'passwordsafe/registry.html', {
            'form': form,
        })
    def post(self, request, *args, **kwargs):
        form = RegistryForm(request.POST)
        if form.is_valid():
            loginname = form.cleaned_data['loginname']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            user = User.objects.create_user(loginname, email, password)
            return self.page_redirect(reverse('passwordsafe:index'), u'注册成功', 2000)
        else:
            return render(request, 'passwordsafe/registry.html', {
                'form': form,
            })

class CheckNameView(MyView):
    def get(self, request, username):
        import re
        pat = re.compile(r'''[0-9a-zA-Z.-_$]{4,}''')
        if not pat.match(username):
            return JsonResponse(errno=100, errmsg=u'用户名不正确')
        user = User.objects.filter(username=username)
        if user:
            return JsonResponse(errno=101, errmsg=u'用户名已存在')
        return JsonResponse()

class LoginView(MyView):
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': LoginForm(),
        })

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            login_user(request, form.cleaned_data['user'])
            url = request.GET.get('next', reverse('passwordsafe:index'))
            return HttpResponseRedirect(url)
        else:
            return render(request, self.template_name, {
                'form': form,
            })

class LogoutView(MyView):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            logout_user(request)
            return self.page_redirect(reverse('passwordsafe:login'), u'登出成功')
        else:
            return HttpResponseRedirect(reverse('passwordsafe:login'))

class AddView(MyView):
    require_auth = True
    def get(self, request):
        return render(request, self.template_name, {
            'form': PasswordForm()
        })
    def post(self, request):
        form = PasswordForm(request.POST)
        if form.is_valid():
            pwd = form.save(commit=False)
            pwd.password = Password.make_password(pwd.password)
            pwd.user = request.user
            pwd.save()
            return self.page_redirect(reverse('passwordsafe:index'), u'添加成功')
        else:
            return render(request, self.template_name, {
                'form': form,
            })

class EditView(MyView):
    require_auth = True
    template_name = 'passwordsafe/add.html'

    def get(self, request, password_id):
        pwd = get_object_or_404(Password, pk=password_id, user=request.user)
        return render(request, self.template_name, {
            'form': PasswordForm(instance=pwd),
        })

    def post(self, request, password_id):
        original = get_object_or_404(Password, pk=password_id, user=request.user)
        form = PasswordForm(request.POST, instance=original)
        if form.is_valid():
            pwd = form.save(commit=False)
            pwd.password = Password.make_password(pwd.password)
            pwd.save()
            return self.page_redirect(reverse('passwordsafe:index'), u'修改成功')
        else:
            return render(request, self.template_name, {
                'form': form,
            })

class DeleteView(MyView):
    require_auth = True

    def get(self, request, password_id):
        pwd = get_object_or_404(Password, pk=password_id, user=request.user)
        pwd.delete()
        return self.page_redirect(reverse('passwordsafe:index'), u'删除成功')

class TestView(MyView):
    require_auth = False

    def get(self, request, tpl):
        return render(request, 'passwordsafe/{}.html'.format(tpl), {})

