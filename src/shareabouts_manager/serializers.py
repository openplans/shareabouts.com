from __future__ import unicode_literals

from django.utils.translation import ugettext as _
from rest_framework import serializers
from shareabouts_manager.models import AccountPackage, UserProfile
from shareabouts_manager.tasks import create_customer, update_customer, subscribe_customer


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
        stripe_token = self.init_data['stripe_token']
        cc_four = self.init_data['cc_four']
        cc_exp = self.init_data['cc_exp']
        cc_type = self.init_data['cc_type']

        # Check whether current user has a customer_id
        if not profile.stripe_id:
            # If there is no customer ID, then schedule one to be created, and
            # then add the credit card once that's done.
            save_cc = create_customer.delay
        else:
            # If there is already a customer ID, then we just have to update
            save_cc = update_customer.delay
        self.task = save_cc(profile.pk, stripe_token, cc_type, cc_four, cc_exp)

    def to_native(self, obj):
        task_serializer = AsyncTaskSerializer(self.task)
        return task_serializer.data


class AsyncTaskSerializer (serializers.Serializer):
    def __init__(self, task_result, *args, **kwargs):
        self.task = task_result
        kwargs['instance'] = task_result
        super(AsyncTaskSerializer, self).__init__(*args, **kwargs)

    def to_native(self, obj):
        details = ''
        if obj.state == 'FAILURE':
            details = str(obj.info).split(':')[0]

        return {
            'status': obj.state.lower(),
            'task': obj.id,
            'details': details,
        }


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

    def save(self, **kwargs):
        subscribe_customer(self.profile, self.data['package'])
        return super(UserProfileSerializer, self).save(**kwargs)
