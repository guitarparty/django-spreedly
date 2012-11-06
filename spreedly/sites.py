from django.conf import settings

DEFAULT_SITE_ALIAS = 'default'

def get_site(site_name=DEFAULT_SITE_ALIAS):
    sites = getattr(settings, 'SPREEDLY_SITES', None)
    site = None
    try:
        site = sites[site_name]
    except KeyError:
        for key, s in sites.items():
            if site_name == s['SPREEDLY_SITE_NAME']:
                site = s
    return site

site = get_site('default')
