from celery import task
from datetime import datetime
from shareabouts_manager.models import CreditCard, UserProfile


@task
def create_customer(profile):
    return profile.pk


@task
def add_user_credit_card(profile, cc_type, cc_four, cc_exp):
    """
    Add a credit card to the user's profile.

    Assumes that:
      * the profile has a stripe customer ID
    """
    if isinstance(profile, (int, basestring)):
        profile = UserProfile.objects.get(pk=profile)

    try:
        cc = profile.credit_card
    except CreditCard.DoesNotExist:
        cc = CreditCard(profile=profile)
    cc.set_info(cc_type, cc_four, cc_exp)
    cc.save()

    return cc.pk
