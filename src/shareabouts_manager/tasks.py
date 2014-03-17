from celery import shared_task
from datetime import datetime
from django.conf import settings
from shareabouts_manager.models import CreditCard, UserProfile
import stripe
import time


@shared_task
def create_customer(profile, cc_token, cc_type, cc_four, cc_exp):
    if isinstance(profile, (int, basestring)):
        profile = UserProfile.objects.get(pk=profile)

    # Set the Stripe API key
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Create the Stripe customer and set the resulting customer ID on the
    # profile model object
    customer = stripe.Customer.create(card=cc_token)
    profile.stripe_id = customer.id
    profile.save()

    add_user_credit_card(cc_type, cc_four, cc_exp)

    return profile.pk


@shared_task
def update_customer(profile, cc_token, cc_type, cc_four, cc_exp):
    if isinstance(profile, (int, basestring)):
        profile = UserProfile.objects.get(pk=profile)

    # Set the Stripe API key
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # Retrieve the customer corresponding to the profile from Stripe and set
    # a new credit card.
    customer = stripe.Customer.retrieve(profile.stripe_id)
    customer.card = cc_token
    customer.save()

    add_user_credit_card(cc_type, cc_four, cc_exp)

    return profile.pk


@shared_task
def add_user_credit_card(profile, cc_type, cc_four, cc_exp):
    """
    Add a credit card to the user's profile.
    Assumes that the profile has a stripe customer ID
    """
    if isinstance(profile, (int, basestring)):
        profile = UserProfile.objects.get(pk=profile)

    # Retrieve or instantiate the credit card model for the profile
    try:
        cc = profile.credit_card
    except CreditCard.DoesNotExist:
        cc = CreditCard(profile=profile)

    # Set and save the given credit card information.
    cc.set_info(cc_type, cc_four, cc_exp)
    cc.save()

    return cc.pk
