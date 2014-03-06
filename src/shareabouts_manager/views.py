from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import resolve_url
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.generic import TemplateView, FormView
from shareabouts_manager.decorators import ssl_required
from shareabouts_manager.forms import UserCreationForm


class LoginRequired (object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequired, self).dispatch(request, *args, **kwargs)


class SSLRequired (object):
    @method_decorator(ssl_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SSLRequired, self).dispatch(request, *args, **kwargs)


class ManagerMixin (SSLRequired, LoginRequired):
    def get_home_url(self, auth):
        if auth is None and self.request.user.is_authenticated():
            auth = self.request.user
        return resolve_url('manager-datasets')


# App
class HelpView (ManagerMixin, TemplateView):
    template_name = 'help.html'


class SignupView (ManagerMixin, SSLRequired, FormView):
    template_name = 'signup.html'
    form_class = UserCreationForm

    def get_initial(self):
        initial = super(SignupView, self).get_initial()
        if 'email' in self.request.GET:
            initial['email'] = self.request.GET['email']
        return initial

    def get_success_url(self):
        return self.get_home_url(self.auth)

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        self.auth = authenticate(username=username, password=password)
        login(self.request, self.auth)
        return super(SignupView, self).form_valid(form)


class PasswordResetView (TemplateView):
    template_name = 'password-reset.html'


class SigninView (ManagerMixin, SSLRequired, FormView):
    template_name = 'signin.html'
    form_class = AuthenticationForm

    def get_context_data(self, **kwargs):
        if 'next' in self.request.GET:
            kwargs['next_url'] = self.request.GET['next']
        return super(SigninView, self).get_context_data(**kwargs)

    def get_success_url(self):
        # Ensure the user-originating redirection url is safe.
        redirect_to = self.request.REQUEST.get('next', self.get_home_url(self.auth))
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
        return redirect_to

    def form_valid(self, form):
        # Okay, security check complete. Log the user in.
        self.auth = form.get_user()
        login(self.request, self.auth)
        return super(SigninView, self).form_valid(form)


class DataSetsView (ManagerMixin, SSLRequired, TemplateView):
    template_name = 'datasets.html'


class IndexView (SSLRequired, TemplateView):
    template_name = 'index.html'


# SEO
class SiteMapView (ManagerMixin, TemplateView):
    template_name = 'sitemap.xml'


# App views
index_view = IndexView.as_view()
datasets_view = DataSetsView.as_view()
signup_view = SignupView.as_view()
signin_view = SigninView.as_view()
password_reset_view = PasswordResetView.as_view()
help_view = HelpView.as_view()
robots_view = TemplateView.as_view(template_name='robots.txt', content_type='text/plain')
sitemap_view = SiteMapView.as_view(content_type='text/xml')
