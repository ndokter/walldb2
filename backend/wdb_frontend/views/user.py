from django.contrib import auth
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse_lazy
from django.urls import reverse_lazy
from django.views.generic import (FormView, ListView, RedirectView,
                                  TemplateView, UpdateView)
from wdb_frontend.forms import LoginForm, RegisterForm


class UserAuthenticationBaseView(FormView):
    form_context_name = None
    template_name = 'wdb_frontend/user/login_register.html'

    def get_context_data(self, **kwargs):
        kwargs.update(
            register_form=RegisterForm(),
            login_form=LoginForm(),
        )

        return super(UserAuthenticationBaseView, self).get_context_data(**kwargs)


class UserLoginView(UserAuthenticationBaseView):
    form_class = LoginForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['login_form'] = context_data['form']

        return context_data

    def form_valid(self, form):
        print('logging in ', form.cleaned_data)
        auth.login(self.request, form.cleaned_data['user'])
        print('logged in')
        return super(UserLoginView, self).form_valid(form)


class UserRegisterView(UserAuthenticationBaseView):
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['register_form'] = context_data['form']

        return context_data

    def form_valid(self, form):
        form.save()

        user = auth.authenticate(
            username=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        auth.login(self.request, user)

        return super(UserRegisterView, self).form_valid(form)


class UserLogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        auth.logout(request)

        return super(UserLogoutView, self)\
            .get(request, *args, **kwargs)