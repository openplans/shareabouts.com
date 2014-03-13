from django.contrib.sessions.backends.cache import SessionStore
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from nose.tools import assert_equal

from django.contrib.auth.models import AnonymousUser
from sa_api_v2.models import DataSet
from shareabouts_manager.models import UserAuth, UserProfile
from shareabouts_manager.views import signup_view, signin_view


class ManagerTestCase (TestCase):
    def setUp(self): self.set_up()
    def tearDown(self): self.tear_down()

    def set_up(self):
        self.factory = RequestFactory()

    def tear_down(self):
        UserAuth.objects.all().delete()
        UserProfile.objects.all().delete()
        DataSet.objects.all().delete()


class SignupViewTests (ManagerTestCase):
    def test_user_is_redirected_home_on_successful_signup(self):
        url = reverse('manager-signup')

        user_data = {
            'username': 'mjumbewu',
            'password': '123',
            'email': 'mjumbewu@example.com',
            'affiliation': 'OpenPlans',
        }

        request = self.factory.post(url, data=user_data)
        request.user = AnonymousUser()
        request.session = SessionStore('session')
        response = signup_view(request)

        # If you get a 200 here, it's probably because of wrong form data.
        assert_equal(response.status_code, 302)
        assert_equal(response.url, reverse('manager-datasets'))

        user_profile = UserProfile.objects.get(auth__username='mjumbewu')
        assert_equal(user_profile.affiliation, 'OpenPlans')


class SigninViewTests (ManagerTestCase):
    def test_user_is_redirected_home_on_successful_signin(self):
        UserAuth.objects.create_user(username='mjumbewu', password='123')
        url = reverse('manager-signin')

        user_data = {
            'username': 'mjumbewu',
            'password': '123',
        }

        request = self.factory.post(url, data=user_data)
        request.user = AnonymousUser()
        request.session = SessionStore('session')
        response = signin_view(request)
        assert_equal(response.status_code, 302)
        assert_equal(response.url, reverse('manager-datasets'))
