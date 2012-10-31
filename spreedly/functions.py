from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.core.cache import cache

from spreedly.models import Plan, Subscription
from spreedly.pyspreedly.api import Client

from spreedly.sites import get_site, DEFAULT_SITE_ALIAS

def sync_plans():
    '''
    Sync subscription plans with Spreedly API
    '''

    for key, site in settings.SPREEDLY_SITES.items():

        client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
        
        for plan in client.get_plans():
            print plan['speedly_id'], site['SPREEDLY_SITE_NAME']
            p, created = Plan.objects.get_or_create(speedly_id=plan['speedly_id'], spreedly_site_name=site['SPREEDLY_SITE_NAME'])
            
            changed = False
            for k, v in plan.items():
                if hasattr(p, k) and not getattr(p, k) == v:
                    setattr(p, k, v)
                    changed = True
            if changed:
                p.save()


def get_subscription(user, site=DEFAULT_SITE_ALIAS):

    site=get_site(site)

    cache_key = 'spreedly-subscription-%d' % user.id

    subscription = cache.get(cache_key)

    if not subscription:
        client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
        data = client.get_info(user.id)
    
        subscription, created = Subscription.objects.get_or_create(
            user=user
        )
        for k, v in data.items():
            if hasattr(subscription, k):
                setattr(subscription, k, v)
        subscription.save()
        cache.set(cache_key, subscription, 60 * 60)

    return subscription

def create_subscription(user, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.get_or_create_subscriber(user.id, user.username)
    return get_subscription(user)
    
def change_subscription(plan, user, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.change_subscription(user.id, plan.pk)
    return get_subscription(user)
    
def get_or_create_subscription(user, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    data = client.get_or_create_subscriber(user.id, user.username)
    
    subscription, created = Subscription.objects.get_or_create(
        user=user
    )
    for k, v in data.items():
        if hasattr(subscription, k):
            setattr(subscription, k, v)
    subscription.save()
    return subscription
    
def check_trial_eligibility(plan, user):
    if plan.plan_type != 'free_trial':
        return False
    try:
        # make sure the user is trial eligable (they don't have a subscription yet, or they are trial_elegible)
        not_allowed = Subscription.objects.get(user=user, trial_elegible=False)
        return False
    except Subscription.DoesNotExist:
        return True

def start_free_trial(plan, user, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    if check_trial_eligibility(plan, user):
        client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
        client.get_or_create_subscriber(user.id, user.username)
        client.subscribe(user.id, plan.pk, trial=True)
        get_subscription(user)
        return True
    else:
        return False
        
def complimentary_time_extension(user, duration_quantity, duration_units, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.complimentary_time_extension(user.id, duration_quantity, duration_units)
    return get_subscription(user)
    
def complimentary_subscription(user, duration_quantity, duration_units, feature_level, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.complimentary_subscription(user.id, duration_quantity, duration_units, feature_level)
    return get_subscription(user)
    
def lifetime_complimentary_subscription(user, feature_level, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.lifetime_complimentary_subscription(user.id, feature_level)
    return get_subscription(user)
    
def add_store_credit(user, amount, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.add_store_credit(user.id, amount)
    return get_subscription(user)
    
def stop_auto_renew(user, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.stop_auto_renew(user.id)
    return get_subscription(user)

def return_url(user, plan=None, trial=False, site=DEFAULT_SITE_ALIAS):
    args = [user.id]
    if plan:
        args.append(plan.pk)
    url = 'http://%s%s' % (Site.objects.get(id=settings.SITE_ID), reverse('spreedly_return', args=args))
    if trial:
        url = url + '?trial=true'
    return url

def allow_free_trial(user, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    client = Client(site['SPREEDLY_AUTH_TOKEN_SECRET'], site['SPREEDLY_SITE_NAME'])
    client.allow_free_trial(user.id)
    return get_subscription(user)

def subscription_url(plan, user, return_url, site=DEFAULT_SITE_ALIAS):
    site=get_site(site)

    return 'https://spreedly.com/%(site_name)s/subscribers/%(user_id)s/subscribe/%(plan_id)s/%(user_username)s?email=%(user_email)s&first_name=%(first_name)s&last_name=%(last_name)s' % {
        'site_name': plan.spreedly_site_name,
        'plan_id': plan.pk,
        'user_id': user.id,
        'user_username': user.username,
        'user_email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'return_url': return_url,
    }
