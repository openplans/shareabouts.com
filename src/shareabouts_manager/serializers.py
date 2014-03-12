from __future__ import unicode_literals

from rest_framework import serializers
from shareabouts_manager.models import AccountPackage


class AccountPackageSerializer (serializers.ModelSerializer):
    class Meta:
        model = AccountPackage
        exclude = ('id', 'stripe_id',)
