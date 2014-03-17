from celery import shared_task
from django.conf import settings
from shareabouts_manager.models import AccountPackage, UserProfile
import stripe


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

    profile.add_credit_card(cc_type, cc_four, cc_exp)

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

    profile.add_credit_card(cc_type, cc_four, cc_exp)

    return profile.pk


@shared_task
def subscribe_customer(profile, package):
    if isinstance(profile, (int, basestring)):
        profile = UserProfile.objects.get(pk=profile)

    if isinstance(package, (int, basestring)):
        package = AccountPackage.objects.get(slug=package)

    # Set the Stripe API key
    stripe.api_key = settings.STRIPE_SECRET_KEY

    # TODO: Any of the following could raise a StripeError if there is no plan
    #       on stripe corresponding to the package's stripe_id (i.e., Stripe's
    #       information is out of sync with ours). We should handle that.
    #
    #       ... or maybe it's an InvalidRequestError. Check.

    customer = stripe.Customer.retrieve(profile.stripe_id)
    if profile.package is None:
        # Create a subscription for the customer
        customer.subscriptions.create(plan=package.stripe_id)
    else:
        # Update the customer's existing subscription (NOTE: this line assumes
        # that the customer has exactly one subscription).
        try:
            subscription = customer.subscriptions.all().data[0]
            # TODO: If the customer has MORE than one subscription, then we
            #       should probably bail and tell them to contact us.
        except IndexError:
            customer.subscriptions.create(plan=package.stripe_id)
        else:
            subscription.plan = package.stripe_id
            subscription.save()

    profile.package = package
    profile.save()

    return profile.pk
