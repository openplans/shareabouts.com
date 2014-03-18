from __future__ import unicode_literals, division

from celery.result import AsyncResult
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import redirect_to_login
from django.core.urlresolvers import reverse
from django.shortcuts import resolve_url, redirect
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views.generic import TemplateView, FormView, View
from sa_api_v2.models import DataSet
from sa_api_v2.serializers import DataSetSerializer
from shareabouts_manager.decorators import ssl_required
from shareabouts_manager.forms import UserCreationForm
from shareabouts_manager.mixins import ValidateInputMixin, JSONResponseMixin
from shareabouts_manager.models import AccountPackage, UserProfile
from shareabouts_manager.serializers import AccountPackageSerializer, UserProfileSerializer, CCInformationSerializer, AsyncTaskSerializer


class ProfileRequired (object):
    def dispatch(self, request, *args, **kwargs):
        if self.get_profile() is None:
            path = request.get_full_path()
            return redirect_to_login(path)
        return super(ProfileRequired, self).dispatch(request, *args, **kwargs)


class SSLRequired (object):
    @method_decorator(ssl_required)
    def dispatch(self, request, *args, **kwargs):
        return super(SSLRequired, self).dispatch(request, *args, **kwargs)


class ManagerMixin (SSLRequired):
    def get_home_url(self, auth):
        if auth is None and self.request.user.is_authenticated():
            auth = self.request.user
        return resolve_url('manager-datasets')

    def get_profile(self):
        if self.request.user.is_authenticated():
            try:
                return self.request.user.profile
            except UserProfile.DoesNotExist:
                return None
        else:
            return None

    def get_package_queryset(self):
        return AccountPackage.objects.all().order_by('price')

    def get_context_data(self, **kwargs):
        context = super(ManagerMixin, self).get_context_data(**kwargs)

        packages = self.get_package_queryset()
        profile = self.get_profile()

        # Add dataset details to the context
        package_serializer = AccountPackageSerializer(packages)
        package_data = package_serializer.data

        context['packages'] = package_data
        context['profile'] = profile

        return context


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


class DataSetsView (ManagerMixin, ProfileRequired, SSLRequired, TemplateView):
    template_name = 'datasets.html'

    def get_datasets_queryset(self, owner):
        return DataSet.objects.filter(owner=owner).prefetch_related('keys')

    def get_context_data(self, **kwargs):
        context = super(DataSetsView, self).get_context_data(**kwargs)

        if self.request.user.is_authenticated():
            owner = self.request.user
            datasets = self.get_datasets_queryset(owner)

            # Add dataset details to the context
            datasets_serializer = DataSetSerializer(datasets)
            datasets_serializer.context = {'request': self.request, 'view': self}
            datasets_data = datasets_serializer.data

            # Add the current profile to the context
            profile = self.get_profile();
            profile_serializer = UserProfileSerializer(profile)
            profile_data = profile_serializer.data

            context['username'] = owner.username
            context['datasets_data'] = datasets_data
            context['profile_data'] = profile_data

        return context


class ProfileView (ManagerMixin, ProfileRequired, SSLRequired, ValidateInputMixin, TemplateView):
    template_name = 'profile.html'
    validator_class = UserProfileSerializer

    def get_success_url(self):
        return reverse('manager-profile')

    def get_validator_args(self):
        return (self.request.user.profile,)

    def on_valid(self, validator):
        validator.save()
        return super(ProfileView, self).on_valid(validator)

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)

        profile = self.get_profile();
        profile_serializer = UserProfileSerializer(profile)
        profile_data = profile_serializer.data

        context['profile_data'] = profile_data
        return context


class SetCardInfoView (ManagerMixin, ProfileRequired, SSLRequired, ValidateInputMixin, View):
    validator_class = CCInformationSerializer

    def on_valid(self, validator):
        validator.save(self.request.user.profile)
        return super(SetCardInfoView, self).on_valid(validator)


class TaskStatusView (SSLRequired, JSONResponseMixin, View):
    def get(self, request, task_id):
        result = AsyncResult(task_id)
        serializer = AsyncTaskSerializer(result)
        return self.render_to_json_response(serializer.data)


class IndexView (ManagerMixin, SSLRequired, TemplateView):
    template_name = 'index.html'

    def get(self, request):
        if self.get_profile() is not None:
            return redirect('manager-datasets')

        return super(IndexView, self).get(request)


# SEO
class SiteMapView (ManagerMixin, TemplateView):
    template_name = 'sitemap.xml'


# App views
index_view = IndexView.as_view()
profile_view = ProfileView.as_view()
datasets_view = DataSetsView.as_view()
signup_view = SignupView.as_view()
signin_view = SigninView.as_view()
password_reset_view = PasswordResetView.as_view()
help_view = HelpView.as_view()
robots_view = TemplateView.as_view(template_name='robots.txt', content_type='text/plain')
sitemap_view = SiteMapView.as_view(content_type='text/xml')

set_card_info_view = SetCardInfoView.as_view()
task_status_view = TaskStatusView.as_view()