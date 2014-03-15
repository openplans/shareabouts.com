from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from rest_framework import serializers
from shareabouts_manager.models import AccountPackage, UserProfile
from shareabouts_manager.tasks import create_customer, add_user_credit_card


class AccountPackageSerializer (serializers.ModelSerializer):
    class Meta:
        model = AccountPackage
        exclude = ('id', 'stripe_id',)


class CCInformationSerializer (serializers.Serializer):
    cc_four = serializers.CharField()
    cc_exp = serializers.CharField()
    cc_type = serializers.CharField()
    stripe_token = serializers.CharField()

    def save(self, profile):
        cc_four = self.data['cc_four']
        cc_exp = self.data['cc_exp']
        cc_type = self.data['c_type']

        # Check whether current user has a customer_id
        if profile.customer_id is None:
            chain = (create_customer.s(profile.pk) |
                     add_user_credit_card.s(cc_four, cc_exp, cc_type))
            chain()
        else:
            add_user_credit_card(profile, cc_four, cc_exp, cc_type)

    def to_native(self, obj):
        return None


class UserProfileSerializer (serializers.ModelSerializer):
    package = serializers.SlugRelatedField(slug_field='slug', required=False)

    class Meta:
        model = UserProfile
        exclude = ('auth', 'stripe_id', 'id')

    def __init__(self, profile, *args, **kwargs):
        self.profile = profile
        kwargs['instance'] = profile
        kwargs.setdefault('partial', True)
        super(UserProfileSerializer, self).__init__(*args, **kwargs)

    def validate_package(self, attrs, source):
        package = attrs['package']
        if package.price > 0:
            # If we're settings a price, then we have to check to make sure the
            # user we're setting it for has a stripe_id.
            if self.profile.stripe_id == '':
                raise serializers.ValidationError(_('Please set your payment information before upgrading your plan.'))
        return attrs
