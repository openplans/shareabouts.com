from datetime import date
from django.test import TestCase
from nose.tools import assert_equal, assert_false, assert_true, assert_in

from django.contrib.auth.models import AnonymousUser
from shareabouts_manager.models import UserAuth, UserProfile, AccountPackage
from shareabouts_manager.serializers import UserProfileSerializer


class ManagerSerializerTestCase (TestCase):
    def setUp(self): self.set_up()
    def tearDown(self): self.tear_down()

    def set_up(self):
        pass

    def tear_down(self):
        UserAuth.objects.all().delete()
        UserProfile.objects.all().delete()
        AccountPackage.objects.all().delete()


class AddUserCreditCardTests (ManagerSerializerTestCase):
    def test_non_free_package_for_user_with_no_payment_info_is_invalid(self):
        profile = UserProfile()
        package = AccountPackage.objects.create(slug='my-package', price=200)

        serializer = UserProfileSerializer(profile, data={'package': package.slug})
        is_valid = serializer.is_valid()
        assert_false(is_valid)
        assert_in('package', serializer.errors)

    def test_non_free_package_for_user_with_payment_info_is_invalid(self):
        profile = UserProfile(stripe_id='123abc')
        package = AccountPackage.objects.create(slug='my-package', price=200)

        serializer = UserProfileSerializer(profile, data={'package': package.slug})
        is_valid = serializer.is_valid()
        assert_true(is_valid)

    def test_assume_partial_updating(self):
        profile = UserProfile.objects.create(email='mjumbewu@example.com', affiliation='OpenPlans', stripe_id='123abc')

        serializer = UserProfileSerializer(profile, data={'email': 'mpoe@example.com'})
        serializer.is_valid()
        updated_profile = serializer.object
        assert_equal(updated_profile.email, 'mpoe@example.com')
        assert_equal(updated_profile.affiliation, 'OpenPlans')
        assert_equal(updated_profile.stripe_id, '123abc')
