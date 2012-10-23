from django.conf import settings

DEFAULT_SITE_ALIAS = 'default'

def get_site(site_name=DEFAULT_SITE_ALIAS):
    sites = getattr(settings, 'SPREEDLY_SITES', None)
    site = sites[site_name]
    return site

site = get_site('default')
