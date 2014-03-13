from __future__ import unicode_literals

from rest_framework import serializers
from shareabouts_manager.models import AccountPackage
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


class UserAccountPackageSerializer (serializers.Serializer):
    package = serializers.SlugRelatedField(slug_field='slug')
