from datetime import date
from django.test import TestCase
from nose.tools import assert_equal

from django.contrib.auth.models import AnonymousUser
from shareabouts_manager.models import UserAuth, UserProfile, CreditCard
from shareabouts_manager.tasks import add_user_credit_card


class ManagerTaskTestCase (TestCase):
    def setUp(self): self.set_up()
    def tearDown(self): self.tear_down()

    def set_up(self):
        pass

    def tear_down(self):
        UserAuth.objects.all().delete()
        UserProfile.objects.all().delete()


class AddUserCreditCardTests (ManagerTaskTestCase):
    def test_adds_users_card(self):
        auth = UserAuth.objects.create()
        profile = UserProfile.objects.create(auth=auth)

        add_user_credit_card(profile, 'Visa', '2424', date(2014, 3, 13))

        cc = CreditCard.objects.all().get(profile=profile)

        assert_equal(cc.four, '2424')
        assert_equal(cc.type, 'Visa')
        assert_equal(cc.exp.month, 3)
        assert_equal(cc.exp.year, 2014)

    def test_can_use_profile_id(self):
        auth = UserAuth.objects.create()
        profile = UserProfile.objects.create(auth=auth)

        add_user_credit_card(profile.id, 'Visa', '2424', date(2014, 3, 13))

        cc = CreditCard.objects.all().get(profile=profile)

        assert_equal(cc.four, '2424')
        assert_equal(cc.type, 'Visa')
        assert_equal(cc.exp.month, 3)
        assert_equal(cc.exp.year, 2014)

    def test_can_use_exp_month_string(self):
        auth = UserAuth.objects.create()
        profile = UserProfile.objects.create(auth=auth)

        add_user_credit_card(profile, 'Visa', '2424', '03/14')

        cc = CreditCard.objects.all().get(profile=profile)

        assert_equal(cc.four, '2424')
        assert_equal(cc.type, 'Visa')
        assert_equal(cc.exp.month, 3)
        assert_equal(cc.exp.year, 2014)

    def test_can_use_exp_month_string_with_4digit_year(self):
        auth = UserAuth.objects.create()
        profile = UserProfile.objects.create(auth=auth)

        add_user_credit_card(profile, 'Visa', '2424', '03/2014')

        cc = CreditCard.objects.all().get(profile=profile)

        assert_equal(cc.four, '2424')
        assert_equal(cc.type, 'Visa')
        assert_equal(cc.exp.month, 3)
        assert_equal(cc.exp.year, 2014)

    def test_can_use_exp_month_string_with_1digit_month(self):
        auth = UserAuth.objects.create()
        profile = UserProfile.objects.create(auth=auth)

        add_user_credit_card(profile, 'Visa', '2424', '3/14')

        cc = CreditCard.objects.all().get(profile=profile)

        assert_equal(cc.four, '2424')
        assert_equal(cc.type, 'Visa')
        assert_equal(cc.exp.month, 3)
        assert_equal(cc.exp.year, 2014)
