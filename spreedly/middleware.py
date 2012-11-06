from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from spreedly.models import Subscription
import spreedly.settings as spreedly_settings
from spreedly import sites

class SpreedlyMiddleware(object):
    '''
    Checks if user is legible to use the website, i.e. has an active
    subscription.
    '''
    def process_request(self, request):
        spreedly_site = None
        if hasattr(request, 'session'):
            spreedly_site = request.session.get('spreedly_site', None)
            if spreedly_site in settings.SPREEDLY_SITES.keys() and spreedly_site is not None:
                request.spreedly_site = spreedly_site
        else:
            spreedly_site = request.COOKIES.get('spreedly_site')
            if spreedly_site in settings.SPREEDLY_SITES.keys() and spreedly_site is not None:
                request.spreedly_site = spreedly_site

        if spreedly_site is None:
            request.spreedly_site = sites.DEFAULT_SITE_ALIAS

        print request.spreedly_site
        
        if spreedly_settings.SPREEDLY_LOCK_TYPE == 'whitelist':
            allowed = False
            for path in spreedly_settings.SPREEDLY_ALLOWED_PATHS + [spreedly_settings.SPREEDLY_URL, settings.LOGIN_URL]:
                if request.path.startswith(path):
                    allowed = True
            
        elif spreedly_settings.SPREEDLY_LOCK_TYPE == 'blacklist':
            allowed = True
            for path in spreedly_settings.SPREEDLY_BLOCKED_PATHS:
                if request.path.startswith(path):
                    allowed = False
        if not allowed:
            if not request.user.is_authenticated():
                if spreedly_settings.SPREEDLY_USERS_ONLY:
                    if spreedly_settings.SPREEDLY_ANONYMOUS_SHOULD_LOGIN:
                        return HttpResponseRedirect(settings.LOGIN_URL)
                    return HttpResponseRedirect(spreedly_settings.SPREEDLY_URL)
            elif request.user.is_authenticated() \
                and not Subscription.objects.has_active(request.user):
                    return HttpResponseRedirect(spreedly_settings.SPREEDLY_URL)
        return
