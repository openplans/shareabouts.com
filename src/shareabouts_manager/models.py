from __future__ import unicode_literals

from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.utils.translation import ugettext as _

UserAuth = get_user_model()


class _TimeStampedModel (models.Model):
    created_at = models.DateTimeField(default=now, blank=True)
    updated_at = models.DateTimeField(default=now, blank=True)

    class Meta:
        abstract = True

    def save(self, update_times=True, *args, **kwargs):
        if update_times:
            if self.pk is None: self.created_at = now()
            self.updated_at = now()
        super(_TimeStampedModel, self).save(*args, **kwargs)


class _BaseAccountProperties (models.Model):
    max_datasets = models.IntegerField(null=True, blank=True)
    max_places = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class AccountPackage (_TimeStampedModel, _BaseAccountProperties):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(decimal_places=0, max_digits=10)
    stripe_id = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class UserProfile (_TimeStampedModel):
    """
    This profile contains data used to administer a dataset owner's account.
    It's the anchor for any information relevant to managing:
    * dataset provision
    * data exports
    * account payments
    """
    auth = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', null=True, blank=True, on_delete=models.CASCADE)
    fullname = models.CharField(_('Full name'), max_length=128, blank=True, help_text=_('The full name of the person or organization'))
    email = models.EmailField(_('Email address'), blank=True)
    affiliation = models.CharField(max_length=256, blank=True, default='')
    stripe_id = models.CharField(max_length=50, blank=True)

    package = models.ForeignKey(AccountPackage, related_name='profiles', null=True, blank=True)
    # overrides (reverse, AccountOverrides)

    def __str__(self):
        return self.fullname

    def can_pay(self):
        return self.stripe_id not in (None, '')

    @property
    def credit_card(self):
        try: return self.credit_cards.all()[0]
        except IndexError: raise CreditCard.DoesNotExist()


class CreditCard (_TimeStampedModel):
    profile = models.ForeignKey(UserProfile, related_name='credit_cards')
    type = models.CharField(_('Type of credit card'), max_length=30)
    four = models.CharField(_('Last four digits'), max_length=4)
    exp = models.DateField(_('Expiration month'), max_length=5)

    def set_info(self, cc_type, cc_four, cc_exp):
        if isinstance(cc_exp, basestring):
            try:
                # 2-digit year?
                cc_exp = datetime.strptime(cc_exp, '%m/%y').date()
            except ValueError:
                # 4-digit year?
                cc_exp = datetime.strptime(cc_exp, '%m/%Y').date()

        self.type = cc_type
        self.four = cc_four
        self.exp = cc_exp


class AccountOverrides (_BaseAccountProperties):
    profile = models.OneToOneField(UserProfile, related_name='overrides')
